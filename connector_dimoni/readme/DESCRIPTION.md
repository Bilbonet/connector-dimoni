This module adds an OCA Connector backend for importing selected master data from
Dimoni through an MSSQL `base.external.dbsource` connection. The backend stores
the Dimoni company scope (`GRP_ID`) and uses connector bindings to keep the link
between Dimoni `ROW_ID` values and Odoo records.

The implemented imports cover Dimoni companies, product templates and partners.
Products can be imported by Dimoni product code into `product.template`, while
partners can be imported by Dimoni partner code into `res.partner`. Imported
records can be refreshed from their Dimoni binding.
