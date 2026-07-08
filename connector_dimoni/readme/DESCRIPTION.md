This module adds an OCA Connector backend for importing selected master data from
Dimoni through an MSSQL `base.external.dbsource` connection. The backend stores
the Dimoni company scope (`GRP_ID`) and uses connector bindings to keep the link
between Dimoni `ROW_ID` values and Odoo records.

The implemented imports cover Dimoni companies, product templates, partners,
partner bank accounts and direct debit mandates. Products can be imported by
Dimoni product code into `product.template`, while partners can be imported by
Dimoni partner code into `res.partner`.

When a partner is imported or refreshed, the connector also imports its bank
accounts into `res.partner.bank` and creates or updates the related banking
mandates when Dimoni provides mandate reference and signature date data.
Imported records can be refreshed from their Dimoni binding.
