"""Manage settings.

class RequestsClient(HTTPClient):
    def request(  # implement request for HTTPClient

        if getattr(self._thread_local, "session", None) is None:
            self._thread_local.session = self._session or requests.Session()

                result = self._thread_local.session.request(
                    method,
                    url,
                    headers=headers,
                    data=post_data,
                    timeout=self._timeout,
                    stream=stream,
                    **kwargs,
                )
        return content, status_code, result.headers, stream
"""
# pylint: disable=invalid-name

import re
from pydantic import BaseSettings, validator
import requests

from logzero import logger


class Settings(BaseSettings):  # pylint: disable=too-few-public-methods
    """Manage api-key and log-level."""

    http_proxy: str = ""
    https_proxy: str = ""
    api_key: str = ""

    class Config:  # pylint: disable=too-few-public-methods
        """Read envs and env."""

        env_prefix = "OPENAI_"
        env_file = ".env"
        env_file_encoding = "utf-8"

        logger.info("env_prefix: %s, env_file: %s", env_prefix, env_file)

    @validator("api_key")
    def validate_apikey(cls, v, values):  # pylint: disable=no-self-use
        """Validate apikey.

        set OPENAI_API_KEY=your_openai_key
        curl -H "Authorization: Bearer %OPENAI_API_KEY%" https://api.openai.com/v1/engines
        # linux and friends:
        # export OPENAI_API_KEY=your_openai_key
        # curl -H "Authorization: Bearer $OPENAI_API_KEY" https://api.openai.com/v1/engines
        """
        version = "v1"
        url = f"https://api.openai.com/{version}/engines"

        # logger.debug("validate_apikey v: %s", v)
        # logger.debug("validate_apikey values: %s", values)

        try:
            v = str(v).strip()
        except Exception as exc:
            logger.warning(exc)
            v = ""
        if not re.match(r"\w{2}-\w{48}", v):
            logger.warning(
                "My Api-Key looks like xx-xxxxxxxxx "
                "(48 letters). Yours doesn't. "
                "We let it pass tho. "
                "It's unlikely you'll pass the next check. "
            )

        # probe opanai server
        headers = {"Authorization": f"Bearer {v}"}

        # logger.debug("http_proxy: %s", http_proxy)
        # logger.debug("validate_apikey v: %s", v)

        # return v

        proxies = {}
        if values["http_proxy"]:  # should validate http[s]_proxy
            proxies.update({"http_proxy": values["http_proxy"]})
        if values["https_proxy"]:
            proxies.update({"https_proxy": values["https_proxy"]})

        logger.info("proxies: %s", proxies)

        try:
            resp = requests.get(
                url,
                headers=headers,
                proxies=proxies,
            )
            resp.raise_for_status()
        except requests.exceptions.HTTPError as exc:
            logger.error(" Errors: %s", exc)
        except Exception as exc:
            logger.error(exc)
            logger.warning(
                "Unable to access opanai. "
                "Check your network, proxies (if set), opanai-api-key "
                "and try again. "
            )
            # raise SystemExit(str(exc)) from exc
            logger.error(" Errors: %s", exc)
            # return str(exc)

        # logger.debug(" resp.json(): %s", resp.json())
        _ = "*" * (len(v) - 10)
        _ = f"{v[:5]}{_}{v[-5:]}"
        # logger.info("\n\tur-api-key: %s", _)
        logger.info("%s", _)

        return v
