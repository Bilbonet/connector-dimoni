- Add scheduled or batch synchronization if imports need to run for more than
  one product or partner code at a time.
- Add concrete export flows if data must be sent from Odoo back to Dimoni. The
  module currently only provides generic exporter scaffolding.
- Extend the mapped fields when more Dimoni columns are required. The current
  mappings cover the fields used by the product, partner and company importers.
- Add automated tests for backend scoping, binding reuse, field mapping and
  refresh behavior.
