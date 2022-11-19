# Copyright 2017 Akretion (http://www.akretion.com).
# @author Sébastien BEAU <sebastien.beau@akretion.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

import os
import urllib

from odoo import _
from odoo.exceptions import UserError

from odoo.addons.component.core import Component


class HttpStorageBackend(Component):
    _name = "http.adapter"
    _inherit = "base.storage.adapter"
    _usage = "http"

    def add(self, relative_path, data, **kwargs):
        raise UserError(_("http backend do not support adding element"))

    def get(self, relative_path, **kwargs):
        full_path = os.path.join(self.collection.base_url, relative_path)
        return urllib.request.urlopen(full_path).read()

    def list(self, relative_path=""):
        raise UserError(_("http backend do not support listing element"))

    def delete(self, relative_path):
        pass
