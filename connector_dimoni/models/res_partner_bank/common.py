# Copyright 2026 Jesus Ramiro <jesus@bilbonet.net>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
from odoo import fields, models

from odoo.addons.component.core import Component


class ResPartnerBank(models.Model):
    _inherit = "res.partner.bank"

    dimoni_binding_ids = fields.One2many(
        comodel_name="dimoni.res.partner.bank",
        inverse_name="odoo_id",
        string="Dimoni Bindings",
    )


class DimoniResPartnerBank(models.Model):
    _name = "dimoni.res.partner.bank"
    _inherit = "dimoni.binding"
    _inherits = {"res.partner.bank": "odoo_id"}
    _description = "Dimoni Partner Bank Account Binding"
    _rec_name = "acc_number"

    odoo_id = fields.Many2one(
        comodel_name="res.partner.bank",
        string="Bank Account",
        readonly=True,
        required=True,
        ondelete="cascade",
    )


class DimoniResPartnerBankAdapter(Component):
    _name = "dimoni.res.partner.bank.adapter"
    _inherit = "dimoni.backend.adapter"
    _apply_on = "dimoni.res.partner.bank"
    _dimoni_src = "FACDC"
    _dimoni_bank_src = "FCTAC"

    def search_for_partner(self, *, partner_ref, id_fiscal):
        query = f"""
            SELECT
                d.ROW_ID,
                d.GRP_ID,
                d.CodCta,
                d.SNHabCCC,
                d.Referen,
                d.FecFirma,
                d.TipoAdeu,
                f.ROW_ID AS FCTAC_ROW_ID,
                f.IdFiscal,
                f.DC_IBAN,
                f.Entidad,
                f.Agencia,
                f.DigCtrol,
                f.NumCta,
                f.CodSwift
            FROM {self._dimoni_src} d
            INNER JOIN {self._dimoni_bank_src} f
                ON LTRIM(RTRIM(d.Entidad)) = LTRIM(RTRIM(f.Entidad))
               AND LTRIM(RTRIM(d.Agencia)) = LTRIM(RTRIM(f.Agencia))
               AND LTRIM(RTRIM(d.DigCtrol)) = LTRIM(RTRIM(f.DigCtrol))
               AND LTRIM(RTRIM(d.NumCta)) = LTRIM(RTRIM(f.NumCta))
               AND UPPER(LTRIM(RTRIM(f.IdFiscal))) = :id_fiscal
            WHERE d.GRP_ID = :grp_id
              AND LTRIM(RTRIM(d.CodCta)) = :partner_ref
        """
        return self._execute_dicts(
            query=query,
            params=self._backend_scope_params(
                partner_ref=partner_ref.strip(),
                id_fiscal=id_fiscal.strip().upper(),
            ),
            columns=[
                "ROW_ID",
                "GRP_ID",
                "CodCta",
                "SNHabCCC",
                "Referen",
                "FecFirma",
                "TipoAdeu",
                "FCTAC_ROW_ID",
                "IdFiscal",
                "DC_IBAN",
                "Entidad",
                "Agencia",
                "DigCtrol",
                "NumCta",
                "CodSwift",
            ],
        )

    def get_by_row_id(self, row_id):
        query = f"""
            SELECT
                d.ROW_ID,
                d.GRP_ID,
                d.CodCta,
                d.SNHabCCC,
                d.Referen,
                d.FecFirma,
                d.TipoAdeu,
                f.ROW_ID AS FCTAC_ROW_ID,
                f.IdFiscal,
                f.DC_IBAN,
                f.Entidad,
                f.Agencia,
                f.DigCtrol,
                f.NumCta,
                f.CodSwift
            FROM {self._dimoni_src} d
            INNER JOIN {self._dimoni_bank_src} f
                ON LTRIM(RTRIM(d.Entidad)) = LTRIM(RTRIM(f.Entidad))
               AND LTRIM(RTRIM(d.Agencia)) = LTRIM(RTRIM(f.Agencia))
               AND LTRIM(RTRIM(d.DigCtrol)) = LTRIM(RTRIM(f.DigCtrol))
               AND LTRIM(RTRIM(d.NumCta)) = LTRIM(RTRIM(f.NumCta))
            WHERE d.GRP_ID = :grp_id
              AND d.ROW_ID = :row_id
        """
        return self._execute_dicts(
            query=query,
            params=self._backend_scope_params(row_id=row_id),
            columns=[
                "ROW_ID",
                "GRP_ID",
                "CodCta",
                "SNHabCCC",
                "Referen",
                "FecFirma",
                "TipoAdeu",
                "FCTAC_ROW_ID",
                "IdFiscal",
                "DC_IBAN",
                "Entidad",
                "Agencia",
                "DigCtrol",
                "NumCta",
                "CodSwift",
            ],
        )
