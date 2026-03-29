from odoo.addons.component.core import Component
from odoo.addons.connector.components.binder import Binder
from odoo.addons.connector.components.mapper import ImportMapper


class DimoniBaseConnectorComponent(Component):
    _name = "dimoni.base"
    _inherit = "base.connector"
    _collection = "dimoni.backend"


class DimoniProductBinder(Binder):
    _name = "dimoni.product.binder"
    _inherit = "base.binder"
    _apply_on = "dimoni.product.template"
    _collection = "dimoni.backend"


class DimoniProductImportMapper(ImportMapper):
    _name = "dimoni.product.import.mapper"
    _inherit = "base.import.mapper"
    _apply_on = "dimoni.product.template"
    _collection = "dimoni.backend"

    direct = [
        ("Codigo", "default_code"),
        ("Descripc", "name"),
    ]
