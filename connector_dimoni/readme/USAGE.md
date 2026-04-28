To import Dimoni records:

- Go to *Connector > Dimoni Connector > Backends* and open a backend.
- Click *Import companies* to import the Dimoni companies available in the
  configured database source.
- Select the imported Dimoni company on the backend. This sets the backend
  `GRP_ID`, which is required before importing products or partners.
- Activate the backend. Optionally enable *Default* so the import wizards use it
  by default for the current Odoo company.
- Click *Import product* and enter a Dimoni product code, or click
  *Import partner* and enter a Dimoni partner code.

Product imports create a `dimoni.product.template` binding when the Dimoni
`ROW_ID` is not linked yet and then open the linked `product.template`. If no
binding exists yet, the importer first searches for an existing product template
with the same `default_code` in the backend company scope before creating a new
product template.

Partner imports create a `dimoni.res.partner` binding when the Dimoni `ROW_ID`
is not linked yet and then open the linked `res.partner`. If no binding exists
yet, the importer first searches for an existing partner with the same `ref` in
the backend company scope before creating a new partner.

The product and partner list and kanban views also expose a *Dimoni Import*
button that opens the corresponding import wizard. Imported product and partner
forms include a Dimoni smart button to open their bindings and a refresh action
to fetch the latest data from Dimoni.
