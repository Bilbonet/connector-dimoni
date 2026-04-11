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

    def _get_default_dimoni_backend(self):
        self.ensure_one()
        company = self.company_id or self.env.company
        return self.env["dimoni.backend"].search(
            [
                ("active", "=", True),
                ("default", "=", True),
                ("grp_id", "!=", False),
                ("company_id", "=", company.id),
            ],
            limit=1,
        )

    def action_open_dimoni_product_import_wizard(self):
        self.ensure_one()
        backend = self._get_default_dimoni_backend()
        context = dict(self.env.context)
        if backend:
            context["default_backend_id"] = backend.id
        if self.default_code:
            context["default_product_code"] = self.default_code
        return {
            "name": self.env._("Import product from Dimoni"),
            "type": "ir.actions.act_window",
            "res_model": "dimoni.product.import.wizard",
            "view_mode": "form",
            "target": "new",
            "context": context,
        }

    def action_open_dimoni_products(self):
        self.ensure_one()
        products = self.dimoni_binding_ids
        if not products:
            return {"type": "ir.actions.act_window_close"}
        action = {
            "type": "ir.actions.act_window",
            "name": self.env._("Dimoni Products"),
            "res_model": "dimoni.product.template",
            "target": "current",
        }
        if len(products) == 1:
            action.update(
                {
                    "view_mode": "form",
                    "res_id": products.id,
                }
            )
            return action
        action.update(
            {
                "view_mode": "list,form",
                "domain": [("odoo_id", "=", self.id)],
                "context": {"default_odoo_id": self.id},
            }
        )
        return action


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

    def action_open_import_wizard(self):
        backend = self.backend_id[:1]
        if len(self.backend_id) > 1 or not backend:
            backend = self.env["dimoni.backend"].search(
                [
                    ("active", "=", True),
                    ("default", "=", True),
                    ("grp_id", "!=", False),
                    ("company_id", "=", self.env.company.id),
                ],
                limit=1,
            )
        context = dict(self.env.context)
        if backend:
            context["default_backend_id"] = backend.id
        if len(self) == 1 and self.default_code:
            context["default_product_code"] = self.default_code
        return {
            "name": self.env._("Import product from Dimoni"),
            "type": "ir.actions.act_window",
            "res_model": "dimoni.product.import.wizard",
            "view_mode": "form",
            "target": "new",
            "context": context,
        }


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
