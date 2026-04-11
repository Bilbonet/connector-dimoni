from odoo.addons.component.core import Component


class DimoniProductTemplateImportMapper(Component):
    _name = "dimoni.product.template.import.mapper"
    _inherit = "dimoni.import.mapper"
    _apply_on = "dimoni.product.template"

    direct = [
        ("ROW_ID", "external_id"),
        ("Codigo", "default_code"),
        ("Descripc", "name"),
    ]
