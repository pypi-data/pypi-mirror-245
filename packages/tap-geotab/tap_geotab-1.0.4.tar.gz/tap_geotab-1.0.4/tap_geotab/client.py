"""Custom client handling, including GeotabStream base class."""

from __future__ import annotations

import logging
import uuid
from typing import Iterable

from requests import Response
from singer_sdk.pagination import LegacyStreamPaginator
from singer_sdk.streams import Stream

import mygeotab

class GeotabStream(Stream):
    """Stream class for Geotab streams."""

    @property
    def conn(self):
        client = mygeotab.API(username=self.config["username"], password=self.config["password"], database=self.config["database"])
        client.authenticate()

        return client

    def post_process(
        self,
        row: dict,
        next_token: str,
        context: dict | None = None,  # noqa: ARG002
    ) -> dict | None:
        new_row = row
        new_row['toVersion'] = next_token
        if not hasattr(row, self.primary_keys[0]):
            new_row[self.primary_keys[0]] = uuid.uuid4()
        return new_row

    def get_records(
        self,
        context: dict | None,  # noqa: ARG002
    ) -> Iterable[dict]:
        next_page_token = self.get_starting_replication_key_value(context)

        records = self.conn.call('GetFeed', typeName=self.name, fromVersion=next_page_token or "0")
        next_token = records.get('toVersion')

        for record in records.get('data', []):
            transformed_record = self.post_process(record, next_token, context)
            if transformed_record is None:
                continue
            yield transformed_record

