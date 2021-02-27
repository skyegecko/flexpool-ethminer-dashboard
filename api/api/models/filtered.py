"""
Default response object based on data from getstatdetail
"""
from __future__ import annotations

import itertools
import logging
from decimal import Decimal
from typing import List, Literal, Optional, Set

from pydantic import AnyUrl, BaseModel, parse_obj_as, validator

import api.models.getstatdetail as GSD
from api.settings import settings

LOGGER = logging.getLogger(__name__)


class Connection(BaseModel):
    connected: bool
    switches: int
    uri: AnyUrl
    scheme: str
    protocol: Optional[str]
    user: Optional[str]
    worker: Optional[str]
    password: Optional[str]
    server: str
    port: Optional[int]
    path: Optional[str]

    _base_stratum_schemes: Set[str] = {
        "stratum",
        "stratum1",
        "stratum2",
        "stratum3",
    }
    _base_schemes_other: Set[str] = {
        "http",
        "getwork",
        "stratums",
        "stratumss",
    }
    _base_protocols: Set[str] = {
        "tcp",
        "tls",
        "tls12",
        "ssl",
    }
    _ethminer_url_schemes: Set[str] = (
        _base_stratum_schemes
        | _base_schemes_other
        | {
            "+".join((stratum, prot))
            for stratum, prot in itertools.product(
                _base_stratum_schemes, _base_protocols
            )
        }
    )

    @validator("uri")
    def valid_uri(cls, uri: AnyUrl) -> AnyUrl:
        replace = "xxxxx"

        if uri.scheme not in cls._ethminer_url_schemes:
            raise ValueError("Received URL scheme not recognised")

        if uri.query is not None:
            raise ValueError("At this time URLs with query part are not supported")

        scheme = uri.scheme
        host = uri.host
        user = uri.user
        password = uri.password
        port = uri.port
        path = uri.path

        if user:
            username, _, worker = user.partition(".")
            if username and not settings.show_username:
                LOGGER.debug("Hiding username in URI")
                username = replace
            if worker and not settings.show_workername:
                LOGGER.debug("Hiding worker in URI")
                worker = replace
            user = ".".join((username, worker))
        if password and not settings.show_password:
            LOGGER.debug("Hiding password in URI")
            password = replace
        if path and not settings.show_pathcomponent:
            LOGGER.debug("Hiding path component in URL")
            path = "/" + replace

        uristr = scheme + "://"
        if user:
            uristr += user
            if password:
                uristr += ":" + password
            uristr += "@"
        uristr += host
        if port:
            uristr += ":" + port
        if path:
            uristr += path

        uri = parse_obj_as(AnyUrl, uristr)

        LOGGER.debug("Returning URI: %s", uri)
        return uri

    @validator("scheme")
    def valid_scheme(cls, schm: str) -> str:
        if schm not in cls._base_stratum_schemes | cls._base_schemes_other:
            raise ValueError("Scheme in received URL not recognised")
        return schm

    @validator("protocol")
    def valid_protocol(cls, prot: Optional[str]) -> Optional[str]:
        if prot is not None and prot not in cls._base_protocols:
            raise ValueError("Protocol in received URL not recognised")
        return prot

    @validator("user")
    def strip_user(cls, user: Optional[str]) -> Optional[str]:
        if settings.show_username:
            return user
        return None

    @validator("worker")
    def strip_worker(cls, worker: Optional[str]) -> Optional[str]:
        if settings.show_workername:
            return worker
        return None

    @validator("password")
    def strip_password(cls, password: Optional[str]) -> Optional[str]:
        if settings.show_password:
            return password
        return None

    @validator("path")
    def strip_path(cls, path: Optional[str]) -> Optional[str]:
        if settings.show_pathcomponent:
            return path
        return None

    @classmethod
    def construct_from_gsd(cls, conn: GSD.Connection) -> Connection:
        scheme, _, protocol = conn.uri.scheme.partition("+")
        user: Optional[str] = None
        worker: Optional[str] = None
        if conn.uri.user:
            user, _, worker = conn.uri.user.partition(".")

        port = int(conn.uri.port) if conn.uri.port else None

        return cls(
            connected=conn.connected,
            switches=conn.switches,
            uri=conn.uri,
            scheme=scheme,
            protocol=protocol,
            user=user,
            worker=worker,
            password=conn.uri.password,
            server=conn.uri.host,
            port=port,
            path=conn.uri.path,
        )


class Shares(BaseModel):
    found: int
    rejected: int
    failed: int
    time_since_last: int

    @classmethod
    def construct_from_gsd(cls, shares: List[int]) -> Shares:
        return cls(
            **{field: shares[i] for i, field in enumerate(cls.__fields__.keys())}
        )


class Device(BaseModel):
    index: int
    mode: Literal["OpenCL", "CUDA"]
    type: Literal["CPU", "GPU", "ACCELERATOR"]
    name: str
    pci_id: str
    temp_c: Decimal
    fan_speed_perc: Decimal
    power_w: Decimal
    hashrate_khs: int
    paused: bool
    pause_reason: Optional[str]
    shares: Shares

    @classmethod
    def construct_from_gsd(cls, dev: GSD.Device) -> Device:
        hardware = dev.hardware
        mining = dev.mining

        temp, fan, power = hardware.sensors
        hashrate = int(mining.hashrate, 16)
        shares = Shares.construct_from_gsd(mining.shares)

        return cls(
            index=dev.index,
            mode=dev.mode,
            type=hardware.type,
            name=hardware.name,
            pci_id=hardware.pci,
            temp_c=temp,
            fan_speed_perc=fan,
            power_w=power,
            hashrate_khs=hashrate,
            paused=mining.paused,
            pause_reason=mining.pause_reason,
            shares=shares,
        )


class Host(BaseModel):
    name: str
    runtime_s: int
    version: str

    @classmethod
    def construct_from_gsd(cls, host: GSD.Host) -> Host:
        return cls(
            name=host.name,
            runtime_s=host.runtime,
            version=host.version,
        )


class Mining(BaseModel):
    difficulty: int
    epoch: int
    epoch_changes: int
    hashrate_khs: int
    shares: Shares

    @classmethod
    def construct_from_gsd(cls, mining: GSD.Mining) -> Mining:
        return cls(
            difficulty=mining.difficulty,
            epoch=mining.epoch,
            epoch_changes=mining.epoch_changes,
            hashrate_khs=int(mining.hashrate, 16),
            shares=Shares.construct_from_gsd(mining.shares),
        )


class Monitors(BaseModel):
    resume_temp: int
    pause_temp: int

    @classmethod
    def construct_from_gsd(cls, monitors: GSD.Monitors) -> Monitors:
        return cls(
            resume_temp=monitors.temperatures[0],
            pause_temp=monitors.temperatures[0],
        )


class Filtered(BaseModel):
    connection: Connection
    devices: List[Device]
    host: Host
    mining: Mining
    monitors: Optional[Monitors]

    @classmethod
    def construct_from_gsd(cls, gsd: GSD.GetStatDetail) -> Filtered:
        return cls(
            connection=Connection.construct_from_gsd(gsd.connection),
            devices=[Device.construct_from_gsd(d) for d in gsd.devices],
            host=Host.construct_from_gsd(gsd.host),
            mining=Mining.construct_from_gsd(gsd.mining),
            monitors=Monitors.construct_from_gsd(gsd.monitors)
            if gsd.monitors
            else None,
        )


def _convert_connection(conn: GSD.Connection) -> Connection:
    pass


def _convert_device(dev: GSD.Device) -> Device:
    pass


def _convert_host(host: GSD.Host) -> Host:
    pass


def _convert_mining(mining: GSD.Mining) -> Mining:
    pass


def _convert_monitors(monitors: GSD.Monitors) -> Monitors:
    pass


def convert_from_getstatdetail(gsd: GSD.GetStatDetail) -> Filtered:
    connection = _convert_connection(gsd.connection)
    devices = [_convert_device(d) for d in gsd.devices]
    host = _convert_host(gsd.host)
    mining = _convert_mining(gsd.mining)
    monitors = _convert_monitors(gsd.monitors) if gsd.monitors else None

    return Filtered(
        connection=connection,
        devices=devices,
        host=host,
        mining=mining,
        monitors=monitors,
    )
