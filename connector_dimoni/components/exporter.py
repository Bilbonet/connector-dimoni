# Copyright 2026 Jesus Ramiro <jesus@bilbonet.net>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

import logging

from odoo.addons.component.core import AbstractComponent

_logger = logging.getLogger(__name__)


# Exporters for Dimoni.
# In addition to its export job, an exporter has to:
# * check in Dimoni if the record has been updated more recently than the
#  last sync date and if yes, delay an import
# * call the ``bind`` method of the binder to update the last sync date


class DimoniBaseExporter(AbstractComponent):
    """Base exporter for Dimoni"""

    _name = "dimoni.base.exporter"
    _inherit = ["base.exporter", "base.dimoni.connector"]
    _usage = "record.exporter"

    def __init__(self, environment):
        """
        :param environment: current environment (backend, session, ...)
        :type environment: :py:class:`connector.connector.ConnectorEnvironment`
        """
        super().__init__(environment)
        self.dimoni_id = None
        self.binding_id = None

    def _get_binding(self):
        """Return the raw Odoo data for ``self.binding_id``"""
        return self.model.browse(self.binding_id)


class DimoniExporter(AbstractComponent):
    """A common flow for the exports to Dimoni"""

    _name = "dimoni.exporter"
    _inherit = "dimoni.base.exporter"

    _odoo_field = "odoo_id"

    def __init__(self, environment):
        """
        :param environment: current environment (backend, session, ...)
        :type environment: :py:class:`connector.connector.ConnectorEnvironment`
        """
        super().__init__(environment)
        self.binding = None

    def _has_to_skip(self, binding=False):
        """Return True if the export can be skipped"""
        return False
