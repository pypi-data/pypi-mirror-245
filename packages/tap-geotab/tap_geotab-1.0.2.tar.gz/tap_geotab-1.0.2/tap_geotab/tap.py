"""Geotab tap class."""

from __future__ import annotations

from singer_sdk import Tap
from singer_sdk import typing as th  # JSON schema typing helpers

# TODO: Import your custom stream types here:
from tap_geotab import streams


class TapGeotab(Tap):
    """Geotab tap class."""

    name = "tap-geotab"

    # TODO: Update this section with the actual config values you expect:
    config_jsonschema = th.PropertiesList(
        th.Property(
            "start_date",
            th.DateTimeType,
            description="The earliest record date to sync",
        ),
        th.Property(
            "username",
            th.StringType,
        ),
        th.Property(
            "password",
            th.StringType,
        ),
        th.Property(
            "database",
            th.StringType,
        ),
    ).to_dict()

    def discover_streams(self) -> list[streams.GeotabStream]:
        """Return a list of discovered streams.

        Returns:
            A list of discovered streams.
        """
        return [
            streams.DevicesStream(self),
            streams.StatusDataStream(self),
            streams.DeviceStatusInfoStream(self),
        ]


if __name__ == "__main__":
    TapGeotab.cli()
