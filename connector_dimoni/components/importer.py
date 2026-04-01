# Copyright 2026 Jesus Ramiro <jesus@bilbonet.net>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

import logging

from odoo.addons.component.core import AbstractComponent

_logger = logging.getLogger(__name__)

RETRY_ON_ADVISORY_LOCK = 1  # seconds
RETRY_WHEN_CONCURRENT_DETECTED = 1  # seconds


def import_record():
    pass


def import_batch():
    pass


class DimoniBaseImporter(AbstractComponent):
    _name = "dimoni.base.importer"
    _inherit = ["base.importer", "base.dimoni.connector"]

    def _import_dependency(
        self, dimoni_id, binding_model, importer_class=None, always=False, **kwargs
    ):
        """
        Import a dependency. The importer class is a subclass of
        ``DimoniImporter``. A specific class can be defined.

        :param dimoni_id: id of the dimoni id to import
        :param binding_model: name of the binding model for the relation
        :type binding_model: str | unicode
        :param importer_cls: :py:class:`odoo.addons.connector.\
                                        connector.ConnectorUnit`
                             class or parent class to use for the export.
                             By default: DimoniImporter
        :type importer_cls: :py:class:`odoo.addons.connector.\
                                       connector.MetaConnectorUnit`
        :param always: if True, the record is updated even if it already
                       exists,
                       it is still skipped if it has not been modified on
                       Dimoni
        :type always: boolean
        :param kwargs: additional keyword arguments are passed to the importer
        """
        if not dimoni_id:
            return
        if importer_class is None:
            importer_class = DimoniImporter
        binder = self.binder_for(binding_model)
        if always or not binder.to_internal(dimoni_id):
            importer = self.component(usage="record.importer", model_name=binding_model)
            importer.run(dimoni_id, **kwargs)


class DimoniImporter(AbstractComponent):
    """Base importer for Dimoni"""

    _name = "dimoni.importer"
    _inherit = "dimoni.base.importer"
    _usage = "record.importer"

    def __init__(self, environment):
        """
        :param environment: current environment (backend, session, ...)
        :type environment: :py:class:`connector.connector.ConnectorEnvironment`
        """
        super().__init__(environment)
        self.dimoni_id = None
        self.dimoni_record = None
