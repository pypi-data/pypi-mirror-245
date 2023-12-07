"""Stream type classes for tap-geotab."""

from __future__ import annotations

import typing as t
from pathlib import Path

from singer_sdk import typing as th  # JSON Schema typing helpers

from tap_geotab.client import GeotabStream

# TODO: Delete this is if not using json files for schema definition
SCHEMAS_DIR = Path(__file__).parent / Path("./schemas")
# TODO: - Override `UsersStream` and `GroupsStream` with your own stream definition.
#       - Copy-paste as many times as needed to create multiple stream types.


class DevicesStream(GeotabStream):
    """Define custom stream."""

    name = "Device"
    primary_keys: t.ClassVar[list[str]] = ["id"]
    replication_key = "toVersion"
    schema_filepath = SCHEMAS_DIR / "devices.json"

class StatusDataStream(GeotabStream):
    """Define custom stream."""

    name = "StatusData"
    primary_keys: t.ClassVar[list[str]] = ["id"]
    replication_key = "toVersion"
    schema_filepath = SCHEMAS_DIR / "status_data.json"

class DeviceStatusInfoStream(GeotabStream):
    """Define custom stream."""

    name = "DeviceStatusInfo"
    replication_key = "toVersion"
    schema_filepath = SCHEMAS_DIR / "device_status_info.json"