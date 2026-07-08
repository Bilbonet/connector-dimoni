Dimoni stores data for multiple companies in the same database. This connector
keeps each Odoo backend scoped to one imported Dimoni company through `GRP_ID`
and preserves the Dimoni `ROW_ID` on binding records so imports can be rerun
without creating duplicate Odoo products, partners or partner bank accounts.

Partner bank accounts are imported from the company-specific Dimoni relation
table and enriched with global bank account details before creating the Odoo
bank account and, when available, the related direct debit mandate.
