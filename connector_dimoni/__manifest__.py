# Copyright 2026 Jesus Ramiro <jesus@bilbonet.net>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
{
    "name": "Connector Dimoni",
    "summary": "Connector framework base for Dimoni product import",
    "version": "18.0.1.0.0",
    "development_status": "Alpha",
    "category": "Connector",
    "website": "https://github.com/Bilbonet/arrace-custom",
    "author": "Jesus Ramiro (Bilbonet)",
    "maintainers": ["bilbonet"],
    "license": "AGPL-3",
    "depends": [
        "connector",
        "base_external_dbsource_mssql",
        "product",
    ],
    "data": [
        "security/ir.model.access.csv",
        "views/dimoni_backend_views.xml",
        "views/dimoni_company_views.xml",
        "views/dimoni_product_template_views.xml",
        "views/product_template_views.xml",
        "wizard/dimoni_product_import_wizard_views.xml",
    ],
    "assets": {
        "web.assets_backend": [
            "connector_dimoni/static/src/js/*.js",
            "connector_dimoni/static/src/xml/*.xml",
        ],
    },
}
