Configure an external database source using the MSSQL connector provided by
`base_external_dbsource_mssql`.

Create a Dimoni backend from *Connector > Dimoni Connector > Backends* and set:

- the Odoo company using the backend;
- the MSSQL external database source;
- whether raw Dimoni payloads should be stored on binding records.

Before activating a backend, import the Dimoni companies from the backend form
and select one of them. Active backends require a selected Dimoni company because
all product, partner and partner bank relation queries are scoped by its
`GRP_ID`.

Enable *Default* on the active backend that should be preselected by the product
and partner import wizards for the current Odoo company.

Partner bank account imports require Dimoni bank account relation data in
`FACDC` for the selected `GRP_ID` and matching bank account details in `FCTAC`.
The connector builds the IBAN from the Dimoni bank account segments and relies
on `base_bank_from_iban` to resolve bank data from the IBAN when possible.
