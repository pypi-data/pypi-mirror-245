"""Classes and methods to control how Feed2Fedi works."""
import json
import sys
from dataclasses import asdict
from dataclasses import dataclass
from enum import Enum
from pathlib import Path
from typing import Any
from typing import Final
from typing import List
from typing import Optional
from typing import Type
from typing import TypeVar
from typing import Union

import aiohttp
import aiosqlite
import arrow
from minimal_activitypub.client_2_server import ActivityPub
from minimal_activitypub.client_2_server import ActivityPubError

from . import DISPLAY_NAME
from . import FILE_ENCODING
from . import POST_RECORDER_SQLITE_DB
from . import WEBSITE

CACHE_DB_PATH_DEFAULT: Final[str] = "./cache.sqlite"
CACHE_MAX_AGE_DEFAULT_30_DAYS: Final[int] = 30
BOT_POST_TEMPLATE_DEFAULT: Final[str] = r"{title}\n\n{link}"

ConfigClass = TypeVar("ConfigClass", bound="Configuration")
PR = TypeVar("PR", bound="PostRecorder")


class PostVisibility(str, Enum):
    """Visibility values supported by Mastodon for a post."""

    PUBLIC = "public"
    UNLISTED = "unlisted"
    PRIVATE = "private"
    DIRECT = "direct"


@dataclass
class FeedInfo:
    """Dataclass to hold info needed for each feed."""

    url: str
    prefix: Optional[str] = None
    max_attachments: Union[int, str] = "max"


@dataclass
class Configuration:
    """Dataclass to hold configuration settings for Feed2Fedi."""

    feeds: List[FeedInfo]
    fedi_instance: str
    fedi_access_token: str
    cache_max_age: int
    cache_db_path: str
    bot_post_media: bool
    bot_post_visibility: PostVisibility
    bot_post_template: str

    @classmethod
    async def load_config(cls: Type[ConfigClass], config_file_path: Path) -> ConfigClass:
        """Load configuration values from file and create Configuration instance.

        :param config_file_path: File name to load configuration values from
        :returns:
            Configuration instance with values loaded from file_name
        """
        if not config_file_path.exists():
            await cls.create_default_config_file(config_file_path)

        with config_file_path.open(mode="r", encoding=FILE_ENCODING) as config_file:
            config_file_dict = json.load(config_file)

        feeds: List[FeedInfo] = []
        for feed in config_file_dict["feeds"]:
            new_feed = FeedInfo(**feed)
            if new_feed.prefix == "None":
                new_feed.prefix = None
            feeds.append(new_feed)

        new_config = cls(**config_file_dict)
        new_config.bot_post_media = bool(new_config.bot_post_media)
        new_config.bot_post_visibility = PostVisibility(new_config.bot_post_visibility)
        new_config.feeds = feeds

        return new_config

    @classmethod
    async def create_default_config_file(cls, config_file_path: Path) -> None:
        """Create new configuration and save as new config file."""
        instance = Configuration._get_instance()
        access_token = await Configuration._get_access_token(instance=instance)
        new_feed = FeedInfo(url="http://feedparser.org/docs/examples/rss20.xml", prefix=None, max_attachments="max")
        new_config = Configuration(
            feeds=[new_feed],
            fedi_instance=instance,
            fedi_access_token=access_token,
            cache_max_age=CACHE_MAX_AGE_DEFAULT_30_DAYS,
            cache_db_path=CACHE_DB_PATH_DEFAULT,
            bot_post_media=True,
            bot_post_visibility=PostVisibility.PUBLIC,
            bot_post_template=BOT_POST_TEMPLATE_DEFAULT,
        )
        with config_file_path.open(mode="w", encoding=FILE_ENCODING) as config_file:
            json.dump(asdict(new_config), fp=config_file, indent=4)

    @staticmethod
    def _get_instance() -> str:
        """Get instance URL from user.

        :returns:
            URL of fediverse instance.
        """
        instance = input("[...] Please enter the URL for the instance to connect to: ")
        return instance

    @staticmethod
    async def _get_access_token(instance: str) -> str:
        """Get access token from fediverse instance.

        :param instance: URL to fediverse instance
        :returns:
            Access token
        """
        try:
            async with aiohttp.ClientSession() as session:
                # Create app
                client_id, client_secret = await ActivityPub.create_app(
                    instance_url=instance,
                    session=session,
                    user_agent=DISPLAY_NAME,
                    client_website=WEBSITE,
                )

                # Get Authorization Code / URL
                authorization_request_url = await ActivityPub.generate_authorization_url(
                    instance_url=instance,
                    client_id=client_id,
                    user_agent=DISPLAY_NAME,
                )
                print(f"Please go to the following URL and follow the instructions:\n" f"{authorization_request_url}")
                authorization_code = input("[...] Please enter the authorization code: ")

                # Validate authorization code and get access token
                access_token = await ActivityPub.validate_authorization_code(
                    session=session,
                    instance_url=instance,
                    authorization_code=authorization_code,
                    client_id=client_id,
                    client_secret=client_secret,
                )

        except ActivityPubError as error:
            print(f"! Error when setting up Fediverse connection: {error}")
            print("! Cannot continue. Exiting now.")
            sys.exit(1)

        return str(access_token)


class PostRecorder:
    """Record posts, check for duplicates, and deletes old records of posts."""

    LAST_POST_TS: Final[str] = "last-post-timestamp"

    def __init__(self: PR, history_db_path: str = f"./{POST_RECORDER_SQLITE_DB}") -> None:
        """Initialise PostRecord instance.

        :param history_db_path: Location where history db should be stored. Default to current directory (.)
        """
        self.history_db_file = history_db_path
        self.history_db: Optional[aiosqlite.Connection] = None

    async def db_init(self: PR) -> None:
        """Initialise DB connection and tables if necessary."""
        self.history_db = await aiosqlite.connect(database=self.history_db_file)
        # Make sure DB tables exist
        await self.history_db.execute(
            "CREATE TABLE IF NOT EXISTS share " "(url TEXT PRIMARY KEY, shared_ts INT) " "WITHOUT ROWID"
        )
        await self.history_db.execute("CREATE INDEX IF NOT EXISTS index_ts ON share(shared_ts)")
        await self.history_db.execute(
            "CREATE TABLE IF NOT EXISTS settings " "(key TEXT PRIMARY KEY, value) " "WITHOUT ROWID"
        )
        await self.history_db.execute(
            "INSERT OR IGNORE INTO settings (key, value) VALUES (:key, :value)",
            {"key": PostRecorder.LAST_POST_TS, "value": 0},
        )
        await self.history_db.commit()

    async def duplicate_check(self: PR, identifier: str) -> bool:
        """Check identifier can be found in log file of content posted to
        Mastodon.

        :param identifier:
                Any identifier we want to make sure has not already been posted.
                This can be id of reddit post, url of media attachment file to be
                posted, or checksum of media attachment file.

        :returns:
                False if "identifier" is not in log of content already posted to
                Mastodon
                True if "identifier" has been found in log of content.
        """
        if self.history_db is None:
            raise AssertionError("Have you called db_init() first?")

        # check for Shared URL
        cursor = await self.history_db.execute("SELECT * FROM share where url=:url", {"url": identifier})
        if await cursor.fetchone():
            return True

        return False

    async def log_post(
        self: PR,
        shared_url: str,
    ) -> None:
        """Log details about posts that have been published.

        :param shared_url:
                URL of feed item
        """
        if self.history_db is None:
            raise AssertionError("Have you called db_init() first?")

        timestamp = arrow.utcnow().timestamp()
        await self.history_db.execute(
            "INSERT INTO share (url, shared_ts) VALUES (?, ?)",
            (
                shared_url,
                timestamp,
            ),
        )
        await self.history_db.commit()

    async def get_setting(
        self: PR,
        key: str,
    ) -> Any:
        """Retrieve a setting from database.

        :param key: Key to setting stored in DB

        :return: Value of setting. This could be an int, str, or float
        """
        if self.history_db is None:
            raise AssertionError("Have you called db_init() first?")

        cursor = await self.history_db.execute(
            "SELECT value FROM settings WHERE key=:key",
            {"key": key},
        )
        row = await cursor.fetchone()
        if row is None:
            return None

        return row[0]

    async def save_setting(
        self: PR,
        key: str,
        value: Union[int, str, float],
    ) -> None:
        """Save a setting to database.

        :param key: Key to setting stored in DB
        :param value: Value to store as a setting

        :return: None
        """
        if self.history_db is None:
            raise AssertionError("Have you called db_init() first?")

        await self.history_db.execute(
            "INSERT OR REPLACE INTO settings (key, value) VALUES (:key, :value)",
            {"key": key, "value": value},
        )

        await self.history_db.commit()

    async def prune(self, max_age_in_days: int) -> None:
        """Prune entries from db that are older than max_age_in_days.

        :param max_age_in_days: Maximum age of records to keep in DB
        """
        if self.history_db is None:
            raise AssertionError("Have you called db_init() first?")

        max_age_ts = arrow.utcnow().shift(days=-max_age_in_days).timestamp()
        await self.history_db.execute(
            "DELETE FROM share WHERE shared_ts<:max_age_ts",
            {"max_age_ts": max_age_ts},
        )
        await self.history_db.commit()

    async def close_db(self: PR) -> None:
        """Close db connection."""
        if self.history_db:
            await self.history_db.close()

    async def import_urls(self, url_file: Path) -> None:
        """Import URLS from for example the cache.db of feed2toot.

        :param url_file: File path containing one URL per line
        """
        if self.history_db is None:
            raise AssertionError("Have you called db_init() first?")

        line_count = 0
        with url_file.open(mode="r", encoding=FILE_ENCODING) as import_file:
            while entry := import_file.readline():
                await self.log_post(shared_url=entry)
                line_count += 1

        print(f"Imported {line_count} urls")

    async def __aenter__(self):
        """Magic method to enable the use of an 'async with PostRecoder(...) as ...' block
        Ready the cache db for.
        """
        await self.db_init()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Magic method defining what happens when 'async with ...' block finishes.
        Close cache db.
        """
        await self.close_db()


class IgnoringLogger:
    """Logger class that ignores all logging silently."""

    def debug(self, msg):
        """Process debug log messages."""
        # For compatibility with youtube-dl, both debug and info are passed into debug
        # You can distinguish them by the prefix '[debug] '
        if msg.startswith("[debug] "):
            pass
        else:
            self.info(msg)

    def info(self, msg):
        """Process info log messages."""
        pass

    def warning(self, msg):
        """Process warning log messages."""
        pass

    def error(self, msg):
        """Process error log messages."""
        pass
