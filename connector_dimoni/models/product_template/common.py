# Copyright 2026 Jesus Ramiro <jesus@bilbonet.net>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
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
        readonly=True,
        required=True,
        ondelete="cascade",
    )

    def action_refresh(self):
        self.ensure_one()
        with self.backend_id.work_on("dimoni.product.template") as work:
            importer = work.component(usage="record.importer")
            importer.get_product(row_id=self.external_id, force_update=True)


class DimoniProductTemplateAdapter(Component):
    _name = "dimoni.product.template.adapter"
    _inherit = "dimoni.backend.adapter"
    _apply_on = "dimoni.product.template"
    _dimoni_src = "PARTI"

    def search_by_code(self, code):
        query = f"""
            SELECT ROW_ID, GRP_ID, Codigo
            FROM {self._dimoni_src}
            WHERE GRP_ID = :grp_id
              AND LTRIM(RTRIM(Codigo)) = :code
        """
        return self._execute_dicts(
            query=query,
            params=self._backend_scope_params(code=code.strip()),
            columns=["ROW_ID", "GRP_ID", "Codigo"],
        )

    def get_by_row_id(self, row_id):
        query = f"""
            SELECT ROW_ID, GRP_ID, Codigo, Descripc
            FROM {self._dimoni_src}
            WHERE GRP_ID = :grp_id
              AND ROW_ID = :row_id
        """
        return self._execute_dicts(
            query=query,
            params=self._backend_scope_params(row_id=row_id),
            columns=["ROW_ID", "GRP_ID", "Codigo", "Descripc"],
        )
