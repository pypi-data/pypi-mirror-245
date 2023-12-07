"""Classes and methods to collect information needed by Feed2Fedi to make posts on Fediverse instance."""
import asyncio
import os
import re
from pathlib import Path
from typing import Any
from typing import Final
from typing import List
from typing import Optional
from urllib.parse import urlsplit

import aiohttp
import feedparser
from bs4 import BeautifulSoup
from markdownify import markdownify


class FeedReader:
    """Instance hold feed items for RSS/Atom feed passed during instantiation."""

    def __init__(self, feed: str) -> None:
        self.items = feedparser.parse(feed).entries
        self.prepare_items_params()
        self.sort_entries()

    def sort_entries(self) -> None:
        """Sorts entries."""
        if all("published_parsed" in item for item in self.items) and all(
            item["published_parsed"] for item in self.items
        ):
            self.items.sort(key=lambda item: item["published_parsed"])

    def prepare_items_params(self) -> None:
        """Prepare items."""
        for item in self.items:
            item.params = {
                "title": item["title"] if "title" in item else None,
                "published": item["published"] if "published" in item else None,
                "updated": item["updated"] if "updated" in item else None,
                "link": item["link"] if "link" in item else None,
                "author": item["author"] if "author" in item else None,
            }

            if item.has_key("summary"):
                # Let's assume item content is HTML
                item.params["content_html"] = item["summary"]
                item.params["content_markdown"] = markdownify(item["summary"], strip=["img"]).strip()
                item.params["content_plaintext"] = markdownify(item["summary"], convert=["br", "p"]).strip()

    @staticmethod
    def determine_image_url(item: feedparser.FeedParserDict) -> List[str]:
        """Determine URL for article image.

        :param item: Item to determine an image URL for
        :returns:
            List of strings with URL to article image
        """
        IMAGE_SELECTOR: Final[str] = 'img[src]:not(img[src*="emoji"])'

        images: List[str] = []
        if item.has_key("summary"):
            parsed_content = BeautifulSoup(item.get("summary"), features="html.parser")
            images = [image.attrs["src"] for image in parsed_content.select(IMAGE_SELECTOR)]

        if len(images):
            return images

        if item.has_key("description"):
            parsed_content = BeautifulSoup(item.get("description"), features="html.parser")
            images = [image.attrs["src"] for image in parsed_content.select(IMAGE_SELECTOR)]

        if len(images):
            return images

        if image_url := item.get("media_thumbnail", [{}])[0].get("url"):
            images = [image_url]

        if len(images):
            return images

        if image_url := item.get("media_content", [{}])[0].get("url"):
            images = [image_url]

        return images


async def get_file(
    img_url: str,
    file: Any,
) -> Optional[str]:
    """Save a file located at img_url to a file located at filepath.

    :param img_url: url of imgur image to download
    :param file: File to write image to

    :returns:
        mime_type (string): mimetype as returned from URL
    """
    mime_type = await determine_mime_type(img_url=img_url)

    chunk_size = 64 * 1024
    try:
        if not mime_type:
            return None

        async with aiohttp.ClientSession(raise_for_status=True) as client:
            response = await client.get(url=img_url)
            async for data_chunk in response.content.iter_chunked(chunk_size):
                file.write(data_chunk)
            await asyncio.sleep(0)  # allow client session to close before continuing

        return mime_type

    except aiohttp.ClientError as save_image_error:
        print(
            "collect.py - get_file(...) -> None - download failed with: %s" % save_image_error,
        )

    return None


async def determine_mime_type(img_url: str) -> Optional[str]:
    """Determine suitable filename for an image based on URL.

    :param img_url: URL to image to determine a file name for.
    :returns:
        mime-type in a String or None
    """
    # First check if URL starts with http:// or https://
    regex = r"^https?://"
    match = re.search(regex, img_url, flags=0)
    if not match:
        print("Post link is not a full link: %s" % img_url)
        return None

    # Acceptable image formats
    image_formats = (
        "image/png",
        "image/jpeg",
        "image/gif",
        "image/webp",
        "video/mp4",
    )

    file_name = Path(os.path.basename(urlsplit(img_url).path))

    # Determine mime type of linked media
    try:
        async with aiohttp.ClientSession(
            raise_for_status=True,
            read_timeout=30,
        ) as client:
            response = await client.head(url=img_url)
            headers = response.headers
            content_type = headers.get("content-type", None)

    except (aiohttp.ClientError, asyncio.exceptions.TimeoutError) as error:
        print("Error while opening URL: %s " % error)
        return None

    if content_type in image_formats:
        return str(content_type)

    if content_type == "application/octet-stream" and file_name.suffix == ".webp":
        return "image/webp"

    print("URL does not point to a valid image file: %s" % img_url)
    return None
