# Copyright 2026 Jesus Ramiro <jesus@bilbonet.net>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
from odoo.addons.component.core import Component
from odoo.addons.connector.components.mapper import mapping

from .country_codes import DIMONI_COUNTRY_CODES


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

    def _get_country(self, record):
        dimoni_code = str(record.get("Pais") or "").strip()
        if dimoni_code.isdigit() and len(dimoni_code) < 3:
            dimoni_code = dimoni_code.zfill(3)
        country_code = DIMONI_COUNTRY_CODES.get(dimoni_code)
        if not country_code:
            return self.env["res.country"]
        return self.env["res.country"].search(
            [("code", "=", country_code)], limit=1
        )

    @mapping
    def default_values(self, record):
        _record = record
        return {"is_company": True}

    @mapping
    def active(self, record):
        return {"active": str(record.get("Activo", "")).strip() == "1"}

    @mapping
    def country_id(self, record):
        country = self._get_country(record)
        return {"country_id": country.id} if country else {}

    @mapping
    def state_id(self, record):
        province_code = str(record.get("Provinci") or "").strip()
        if province_code.isdigit() and len(province_code) < 2:
            province_code = province_code.zfill(2)
        if len(province_code) != 2:
            return {}

        zip_code = str(record.get("CPostal") or "").strip()
        if zip_code and not zip_code.startswith(province_code):
            return {}

        country = self._get_country(record)
        if not country:
            return {}

        zip_domain = [
            ("country_id", "=", country.id),
            ("state_id", "!=", False),
        ]
        zip_location = self.env["res.city.zip"]
        if zip_code:
            zip_location = zip_location.search(
                [*zip_domain, ("name", "=", zip_code)], limit=1
            )
        if not zip_location:
            zip_location = self.env["res.city.zip"].search(
                [*zip_domain, ("name", "=like", f"{province_code}%")],
                limit=1,
            )
        state = zip_location.state_id
        return {"state_id": state.id} if state else {}

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

    @mapping
    def phone(self, record):
        phone = (record.get("Tlfno_1") or "").strip()
        if not phone:
            return {}
        return {"phone": phone}

    @mapping
    def mobile(self, record):
        mobile = (record.get("Tlfno_2") or "").strip()
        if not mobile:
            return {}
        return {"mobile": mobile}

    @mapping
    def email(self, record):
        email = (record.get("DirEmail") or "").strip()
        if not email:
            return {}
        return {"email": email}

    @mapping
    def website(self, record):
        website = (record.get("DirWeb") or "").strip()
        if not website:
            return {}
        return {"website": website}
