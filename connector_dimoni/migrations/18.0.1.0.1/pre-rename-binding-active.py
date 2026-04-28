# Copyright 2026 Jesus Ramiro <jesus@bilbonet.net>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
from odoo.tools import SQL
from odoo.tools.sql import column_exists, rename_column


def _rename_active_column(cr, table):
    if not column_exists(cr, table, "active"):
        return
    if column_exists(cr, table, "binding_active"):
        cr.execute(
            SQL(
                """
                UPDATE %s
                   SET binding_active = active
                 WHERE binding_active IS DISTINCT FROM active
                """,
                SQL.identifier(table),
            )
        )
        cr.execute(
            SQL(
                "ALTER TABLE %s DROP COLUMN %s",
                SQL.identifier(table),
                SQL.identifier("active"),
            )
        )
        return
    rename_column(cr, table, "active", "binding_active")


def migrate(cr, version):
    for table in (
        "dimoni_company",
        "dimoni_product_template",
        "dimoni_res_partner",
    ):
        _rename_active_column(cr, table)
