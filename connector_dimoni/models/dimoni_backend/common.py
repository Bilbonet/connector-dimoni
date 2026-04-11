from odoo import api, fields, models
from odoo.exceptions import UserError, ValidationError


class DimoniBackend(models.Model):
    _name = "dimoni.backend"
    _inherit = "connector.backend"
    _description = "Dimoni Backend"

    name = fields.Char(
        required=True,
        copy=False,
        default="/",
    )
    company_id = fields.Many2one(
        comodel_name="res.company",
        string="Company",
        required=True,
        default=lambda self: self.env.company,
        help="Company who uses this Dimoni Backend.",
    )
    active = fields.Boolean(default=False)
    default = fields.Boolean(
        default=False,
        copy=False,
        help="Default backend for the company.",
    )
    store_raw_payload = fields.Boolean(
        help="Store Raw Payload (JSON) data for Dimoni records.",
    )
    dbsource_id = fields.Many2one(
        comodel_name="base.external.dbsource",
        string="External DB Source",
        required=True,
        ondelete="restrict",
        domain=[("connector", "=", "mssql")],
    )
    dimoni_company_id = fields.Many2one(
        comodel_name="dimoni.company",
        string="Dimoni Company",
        copy=False,
        ondelete="restrict",
        help="Company imported from Dimoni and used to scope the connector data.",
    )
    grp_id = fields.Char(
        related="dimoni_company_id.grp_id",
        string="Dimoni GRP_ID",
        store=True,
        copy=False,
        readonly=True,
        help="Company key in Dimoni used in database to bind "
             "the records to a specific company",
    )

    _sql_constraints = [
        (
            "dimoni_backend_company_grp_uniq",
            "unique(company_id, grp_id)",
            "A backend already exists for this company and GRP_ID.",
        )
    ]

    @api.constrains("active", "grp_id")
    def _check_active_requires_grp_id(self):
        for record in self:
            if record.active and not record.grp_id:
                raise ValidationError(
                    record.env._(
                        "A backend must have a Dimoni company "
                        "before it can be activated."
                    )
                )

    def action_import_companies(self):
        self.ensure_one()
        if not self.dbsource_id:
            raise UserError(
                self.env._("Please select the Dimoni database source first.")
            )

        previous_grp_id = self.grp_id
        with self.work_on("dimoni.company") as work:
            importer = work.component(usage="record.importer")
            companies = importer.run()

        if not companies:
            raise UserError(
                self.env._(
                    "No companies were found in Dimoni "
                    "for the selected database source."
                )
            )

        selected_company = self.env["dimoni.company"]
        if previous_grp_id:
            selected_company = companies.filtered(
                lambda company: company.grp_id == previous_grp_id
            )[:1]
        if not selected_company and len(companies) == 1:
            selected_company = companies[:1]
        if selected_company:
            self.dimoni_company_id = selected_company.id

        return {
            "type": "ir.actions.act_window",
            "name": "Dimoni Backend",
            "res_model": "dimoni.backend",
            "res_id": self.id,
            "view_mode": "form",
            "target": "current",
        }

    def action_open_product_import_wizard(self):
        self.ensure_one()
        if not self.grp_id:
            raise UserError(
                self.env._(
                    "Import the companies from Dimoni and select one "
                    "on the backend before importing products."
                )
            )
        return {
            "name": "Import product from Dimoni",
            "type": "ir.actions.act_window",
            "res_model": "dimoni.product.import.wizard",
            "view_mode": "form",
            "target": "new",
            "context": {"default_backend_id": self.id},
        }
