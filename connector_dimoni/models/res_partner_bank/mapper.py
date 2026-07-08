# Copyright 2026 Jesus Ramiro <jesus@bilbonet.net>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
from odoo.addons.component.core import Component
from odoo.addons.connector.components.mapper import mapping


class DimoniResPartnerBankImportMapper(Component):
    _name = "dimoni.res.partner.bank.import.mapper"
    _inherit = "dimoni.import.mapper"
    _apply_on = "dimoni.res.partner.bank"

    direct = [
        ("ROW_ID", "external_id"),
    ]

    @staticmethod
    def _clean_segment(value, length=None):
        segment = str(value or "").strip().replace(" ", "")
        if length and segment and segment.isdigit():
            segment = segment.zfill(length)
        return segment

    def _get_acc_number(self, record):
        segments = (
            self._clean_segment(record.get("DC_IBAN"), 4),
            self._clean_segment(record.get("Entidad"), 4),
            self._clean_segment(record.get("Agencia"), 4),
            self._clean_segment(record.get("DigCtrol"), 2),
            self._clean_segment(record.get("NumCta"), 10),
        )
        return "".join(segments).upper()

    @mapping
    def acc_number(self, record):
        acc_number = self._get_acc_number(record)
        return {"acc_number": acc_number} if acc_number else {}
