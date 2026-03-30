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
    dimoni_grp_id = fields.Char(string="Dimoni GRP_ID", required=True)


class DimoniProductAdapter(Component):
    _name = "dimoni.product.adapter"
    _inherit = "base.dimoni.connector"
    _usage = "backend.adapter"
    _apply_on = "dimoni.product.template"

    def _dbsource(self):
        return self.backend_record.dbsource_id

    def _row_to_dict(self, row):
        mapping = getattr(row, "_mapping", None)
        if mapping:
            return dict(mapping)
        if isinstance(row, dict):
            return row
        return {
            "ROW_ID": row[0],
            "GRP_ID": row[1],
            "Codigo": row[2],
            "Descripc": row[3],
        }

    def search_by_code(self, code):
        query = """
            SELECT ROW_ID, GRP_ID, Codigo, Descripc
            FROM PARTI
            WHERE GRP_ID = :grp_id
              AND LTRIM(RTRIM(Codigo)) = :code
        """
        rows = self._dbsource().execute(
            query=query,
            execute_params={
                "grp_id": self.backend_record.dimoni_grp_id,
                "code": code.strip(),
            },
        )
        return [self._row_to_dict(row) for row in rows]
