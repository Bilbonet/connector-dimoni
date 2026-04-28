# Copyright 2026 Jesus Ramiro <jesus@bilbonet.net>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
from odoo.addons.component.core import Component
from odoo.addons.connector.components.mapper import mapping


class DimoniResPartnerImportMapper(Component):
    _name = "dimoni.res.partner.import.mapper"
    _inherit = "dimoni.import.mapper"
    _apply_on = "dimoni.res.partner"

    direct = [
        ("ROW_ID", "external_id"),
        ("Codigo", "ref"),
        ("Razon", "name"),
        ("direccio", "street"),
        ("CPostal", "zip"),
        ("Localida", "city"),
    ]

    @mapping
    def default_values(self, record):
        _record = record
        return {"is_company": True}

    @mapping
    def active(self, record):
        return {"active": str(record.get("Activo", "")).strip() == "1"}

    @mapping
    def comercial(self, record):
        """
        If `Razon` equals `Nombre`, it sets `comercial` to False to avoid storing
        redundant data.
        """
        razon = (record.get("Razon") or "").strip()
        name = (record.get("name") or "").strip()
        if razon and name and razon == name:
            return {"comercial": False}
        return {"comercial": name or False}

    @mapping
    def vat(self, record):
        vat = record.get("Nif")
        if vat in (None, False):
            return False
        vat = str(vat).strip()
        return {"vat": vat}
