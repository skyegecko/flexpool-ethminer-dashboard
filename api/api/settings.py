"""
Import settings from environment variables
"""

import logging
import os
import pprint
import typing
from typing import Callable, Optional, TypeVar

LOGGER = logging.getLogger(__name__)

T = TypeVar("T", bool, int, str)
ValidatorCallable = Callable[[str, str], T]


class _Settings:
    """
    Setup class which imports settings from environment and performs validation.
    """

    def __init__(self) -> None:
        if LOGGER.isEnabledFor(logging.DEBUG):
            props = [
                att
                for att in dir(self.__class__)
                if isinstance(getattr(self.__class__, att), property)
            ]
            settings = {p: getattr(self, p) for p in props}
            LOGGER.debug("Loaded settings:\n%s", pprint.pformat(settings))

    @classmethod
    def _str_to_bool(cls, envvar: str, val: str) -> bool:
        truthy = ("true", "yes", "1")
        falsey = ("false", "no", "0")
        if val.lower() in truthy:
            return True
        if val.lower() in falsey:
            return False
        LOGGER.critical(
            "Could not parse variable %s with value %s as boolean",
            envvar,
            val,
        )
        raise ValueError("Could not parse value to boolean")

    @classmethod
    def _str_to_int(cls, envvar: str, val: str) -> int:
        try:
            return int(val)
        except ValueError:
            LOGGER.critical(
                "Could not parse variable %s with value %s as integer",
                envvar,
                val,
            )
            raise ValueError("Could not parse value to integer")

    def _set_and_get_prop(
        self,
        name: str,
        envvar: str,
        default: T,
        validator: Optional[ValidatorCallable[T]],
    ) -> T:
        try:
            return getattr(self, name)
        except AttributeError:
            envval = os.getenv(envvar)
            if envval is None:
                val: T = default
            else:
                if validator:
                    val = validator(envvar, envval)
                else:
                    val = typing.cast(T, envval)  # typing: ignore
            setattr(self, name, val)
            return val

    @property
    def api_root_path(self) -> str:
        return self._set_and_get_prop("_api_root_path", "API_ROOT_PATH", "", None)

    @property
    def source_address(self) -> str:
        return self._set_and_get_prop("_source_address", "APISOURCE_ADDR", "", None)

    @property
    def source_port(self) -> int:
        return self._set_and_get_prop(
            "_source_port", "APISOURCE_PORT", 0, self._str_to_int
        )

    @property
    def connection_timeout(self) -> int:
        return self._set_and_get_prop(
            "_connection_timeout", "CONNECTION_TIMEOUT", 5, self._str_to_int
        )

    @property
    def connection_keepalive(self) -> int:
        return self._set_and_get_prop(
            "_connection_keepalive", "CONNECTION_KEEPALIVE", 30, self._str_to_int
        )

    @property
    def show_username(self) -> bool:
        return self._set_and_get_prop(
            "_show_username", "SHOW_USERNAME", False, self._str_to_bool
        )

    @property
    def show_password(self) -> bool:
        return self._set_and_get_prop(
            "_show_password", "SHOW_PASSWORD", False, self._str_to_bool
        )

    @property
    def show_workername(self) -> bool:
        return self._set_and_get_prop(
            "_show_workername", "SHOW_WORKERNAME", False, self._str_to_bool
        )

    @property
    def show_pathcomponent(self) -> bool:
        return self._set_and_get_prop(
            "_show_pathcomponent", "SHOW_PATHCOMPONENT", False, self._str_to_bool
        )


settings = _Settings()
