"""
Import settings from environment variables
"""

import logging
import os
import pprint
import re
from typing import Callable, Dict, NamedTuple, Union

LOGGER = logging.getLogger(__name__)


SettingsUnion = Union[bool, int, str]


class _KeyRelation(NamedTuple):
    envvar: str
    default: str
    validator: Callable[[str, str], SettingsUnion]


class _Settings:
    """
    Setup class which imports settings from environment and performs validation.
    """

    def __init__(self) -> None:
        self.keys_and_defaults: Dict[str, _KeyRelation] = {
            "api_root_path": _KeyRelation("API_ROOT_PATH", "", self.noop_validator),
            "source_address": _KeyRelation("APISOURCE_ADDR", "", self.noop_validator),
            "source_port": _KeyRelation("APISOURCE_PORT", "0", self.str_to_int),
            "connection_timeout": _KeyRelation(
                "CONNECTION_TIMEOUT", "5", self.str_to_int
            ),
            "connection_keepalive": _KeyRelation(
                "CONNECTION_KEEPALIVE", "30", self.str_to_int
            ),
            "show_username": _KeyRelation("SHOW_USERNAME", "false", self.str_to_bool),
            "show_password": _KeyRelation("SHOW_PASSWORD", "false", self.str_to_bool),
            "show_workername": _KeyRelation(
                "SHOW_WORKERNAME", "false", self.str_to_bool
            ),
            "show_pathcomponent": _KeyRelation(
                "SHOW_PATHCOMPONENT", "false", self.str_to_bool
            ),
        }

        self.fetch_env()
        self.validate_settings()

    def fetch_env(self) -> None:
        self.env: Dict[str, str] = {}
        for key, keyrel in self.keys_and_defaults.items():
            val = os.getenv(keyrel.envvar, keyrel.default)
            if val == "":
                val = keyrel.default
            self.env[key] = val

    def validate_settings(self) -> None:
        self.settings: Dict[str, SettingsUnion] = {}
        for key in self.env:
            self.settings[key] = self.keys_and_defaults[key].validator(
                key, self.env[key]
            )
        if LOGGER.isEnabledFor(logging.DEBUG):
            LOGGER.debug("Loaded settings:\n%s", pprint.pformat(self.settings))

    def noop_validator(self, key: str, val: str) -> str:
        return val

    def str_to_bool(self, key: str, val: str) -> bool:
        truthy = ("true", "yes", "1")
        falsey = ("false", "no", "0")
        if val.lower() in truthy:
            return True
        if val.lower() in falsey:
            return False
        LOGGER.critical(
            "Could not parse variable %s with value %s as boolean",
            self.keys_and_defaults[key][0],
            val,
        )
        raise ValueError("Could not parse value to boolean")

    def str_to_int(self, key: str, val: str) -> int:
        try:
            return int(val)
        except ValueError:
            LOGGER.critical(
                "Could not parse variable %s with value %s as integer",
                self.keys_and_defaults[key][0],
                val,
            )
            raise ValueError("Could not parse value to integer")


_settings = _Settings()


def __getattr__(name: str) -> SettingsUnion:
    return _settings.settings[name]
