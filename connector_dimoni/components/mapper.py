# Copyright 2026 Jesus Ramiro <jesus@bilbonet.net>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
import json

from odoo import fields

from odoo.addons.component.core import AbstractComponent
from odoo.addons.connector.components.mapper import mapping


class DimoniImportMapper(AbstractComponent):
    _name = "dimoni.import.mapper"
    _inherit = ["base.dimoni.connector", "base.import.mapper"]
    _usage = "import.mapper"

    @staticmethod
    def _prepare_raw_payload(record):
        mapping = getattr(record, "_mapping", None)
        if mapping is not None:
            return dict(mapping)
        if isinstance(record, dict):
            return record
        return {"value": record}

    @mapping
    def sync_metadata(self, record):
        raw_payload = False
        if self.backend_record.store_raw_payload:
            raw_payload = json.dumps(
                self._prepare_raw_payload(record),
                ensure_ascii=False,
                indent=2,
                default=str,
            )

        return {
            "backend_id": self.backend_record.id,
            "sync_date": fields.Datetime.now(),
            "raw_payload": raw_payload,
        }


class DimoniExportMapper(AbstractComponent):
    _name = "dimoni.export.mapper"
    _inherit = ["base.dimoni.connector", "base.export.mapper"]
    _usage = "export.mapper"
