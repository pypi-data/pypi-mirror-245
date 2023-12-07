"""Classes and methods needed to publish posts on a Fediverse instance."""
import asyncio
import tempfile
import traceback
from pathlib import Path
from typing import List
from typing import Optional
from typing import Union

import aiohttp
import arrow
import magic
import yt_dlp
from feedparser import FeedParserDict
from minimal_activitypub.client_2_server import ActivityPub
from minimal_activitypub.client_2_server import ClientError
from minimal_activitypub.client_2_server import RatelimitError

from .collect import FeedReader
from .collect import get_file
from .control import Configuration
from .control import IgnoringLogger
from .control import PostRecorder


class Fediverse:
    """Helper class to publish posts on a fediverse instance from rss feed items."""

    def __init__(self, config: Configuration, post_recorder: PostRecorder) -> None:
        self.config = config
        self.post_recorder = post_recorder

    async def publish(
        self,
        items: List[FeedParserDict],
        prefix: Optional[str] = None,
        max_attachments: Union[int, str] = 1,
    ) -> None:
        """Publish posts to fediverse instance from content in the items list.

        :param items: Rss feed items to post
        :param prefix: Prefix to use to prepend to title when posting
        :param max_attachments: Maximum number of attachments to post, defaults to 1
        """
        async with aiohttp.ClientSession() as session:
            fediverse = ActivityPub(
                instance=self.config.fedi_instance,
                session=session,
                access_token=self.config.fedi_access_token,
            )
            await fediverse.determine_instance_type()
            await fediverse.verify_credentials()

            if isinstance(max_attachments, int):
                max_media = min(fediverse.max_attachments, max_attachments)
            else:
                max_media = fediverse.max_attachments

            for item in items:
                if await self.post_recorder.duplicate_check(identifier=item.link):
                    continue

                status = ""
                if prefix:
                    status += f"{prefix} - "
                status += self.config.bot_post_template.format(**item.params).replace("\\n", "\n")
                media_ids: List[str] = []

                try:
                    # Post media if configured to and media_thumbnail is present with an url
                    if self.config.bot_post_media:
                        media_ids = await Fediverse._post_video(fediverse=fediverse, item=item)

                        if len(media_ids) == 0:
                            media_ids = await Fediverse._post_images(
                                fediverse=fediverse,
                                item=item,
                                max_images=max_media,
                            )

                    posted_status = await fediverse.post_status(
                        status=status,
                        visibility=self.config.bot_post_visibility.value,
                        media_ids=media_ids,
                    )

                    print(f"Posted {posted_status['content']} to Fediverse at\n{posted_status['url']}")

                    await self.post_recorder.log_post(shared_url=item.link)

                except RatelimitError:
                    reset = fediverse.ratelimit_reset
                    seconds = reset.timestamp() - arrow.now().timestamp()
                    print(f'!!! Server "cool down" - waiting for {seconds} seconds (until {reset})')
                    await asyncio.sleep(delay=seconds)

                except ClientError as error:
                    print(f"!!! Encountered error: {error}")
                    traceback.print_tb(error.__traceback__)
                    print("\nLog article to avoid repeat of error")
                    await self.post_recorder.log_post(shared_url=item.link)

    @staticmethod
    async def _post_video(
        fediverse: ActivityPub,
        item: FeedParserDict,
    ) -> List[str]:
        """Post media to fediverse instance and return media ID.

        :param fediverse: ActivityPub api instance
        :param item: Feed item to load media from
        :returns:
            List containing no, one  or multiple strings of the media id after upload
        """
        media_ids: List[str] = []
        filenames: List[str] = []

        ydl_opts = {
            "quiet": "true",
            "logger": IgnoringLogger(),
            "no_warnings": "true",
            "ignoreerrors": "true",
            "outtmpl": "%(id)s.%(ext)s",
        }
        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(item.link, download=True)
                if (ydl_info := ydl.sanitize_info(info)) and ydl_info.get("requested_downloads"):
                    for dl in ydl_info.get("requested_downloads"):
                        if filename := dl.get("filepath"):
                            filenames.append(filename)
        except yt_dlp.utils.DownloadError:
            # Skip and go to next processing type
            pass

        if len(filenames) > 0:
            for filename in filenames:
                mime_type = magic.from_file(filename=filename, mime=True)
                try:
                    if mime_type:
                        with Path(filename).open(mode="rb") as file:
                            media = await fediverse.post_media(file=file, mime_type=mime_type)
                        media_ids.append(media.get("id"))
                except ClientError as error:
                    raise ClientError from error
                finally:
                    Path(filename).unlink()

        return media_ids

    @staticmethod
    async def _post_images(
        fediverse: ActivityPub,
        item: FeedParserDict,
        max_images: int = 1,
    ) -> List[str]:
        """Post media to fediverse instance and return media ID.

        :param fediverse: ActivityPub api instance
        :param item: Feed item to load media from
        :param max_images: number of images to post. Defaults to 1
        :returns:
            List containing no, one  or multiple strings of the media id after upload
        """
        media_ids: List[str] = []
        media_urls = FeedReader.determine_image_url(item)

        for url in media_urls:
            if len(media_ids) == max_images:
                break

            with tempfile.TemporaryFile() as temp_image_file:
                mime_type = await get_file(img_url=url, file=temp_image_file)
                if mime_type:
                    temp_image_file.seek(0)
                    media = await fediverse.post_media(
                        file=temp_image_file,
                        mime_type=mime_type,
                    )
                    media_ids.append(media["id"])

        return media_ids
