from odoo.addons.component.core import Component
from odoo.addons.connector.components.mapper import mapping


class DimoniProductTemplateImportMapper(Component):
    _name = "dimoni.product.template.import.mapper"
    _inherit = "dimoni.import.mapper"
    _apply_on = "dimoni.product.template"

    direct = [
        ("ROW_ID", "external_id"),
        ("Codigo", "default_code"),
        ("Descripc", "name"),
        ("Ampliaci", "description"),
    ]

    @mapping
    def active(self, record):
        return {"active": record.get("Activo") == 1}

    @mapping
    def list_price(self, record):
        sale_price = record.get("Pvp_01")
        if sale_price in (None, ""):
            return {}
        return {"list_price": float(sale_price)}

    @mapping
    def product_type(self, record):
        article_type = record.get("TipoArti")
        if article_type in (4, "4"):
            return {"type": "service", "is_storable": False}
        if article_type in (1, "1"):
            return {"type": "consu", "is_storable": True}
        if article_type in (2, "2", 3, "3", 5, "5"):
            return {"type": "consu", "is_storable": False}
        return {}
