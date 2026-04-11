from odoo import fields, models

from odoo.addons.component.core import Component


class ProductTemplate(models.Model):
    _inherit = "product.template"

    dimoni_binding_ids = fields.One2many(
        comodel_name="dimoni.product.template",
        inverse_name="odoo_id",
        string="Dimoni Bindings",
    )


class DimoniProductTemplate(models.Model):
    _name = "dimoni.product.template"
    _inherit = "dimoni.binding"
    _inherits = {"product.template": "odoo_id"}
    _description = "Dimoni Product Template Binding"

    odoo_id = fields.Many2one(
        comodel_name="product.template",
        string="Product Template",
        required=True,
        ondelete="cascade",
    )


class DimoniProductTemplateAdapter(Component):
    _name = "dimoni.product.template.adapter"
    _inherit = "dimoni.backend.adapter"
    _apply_on = "dimoni.product.template"

    def search_by_code(self, code):
        query = """
            SELECT ROW_ID, GRP_ID, Codigo, Descripc
            FROM PARTI
            WHERE GRP_ID = :grp_id
              AND LTRIM(RTRIM(Codigo)) = :code
        """
        return self._execute_dicts(
            query=query,
            params=self._backend_scope_params(code=code.strip()),
            columns=["ROW_ID", "GRP_ID", "Codigo", "Descripc"],
        )
