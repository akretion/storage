# Copyright 2017 Akretion (http://www.akretion.com).
# @author Sébastien BEAU <sebastien.beau@akretion.com>
# Copyright 2019 Camptocamp SA (http://www.camptocamp.com).
# @author Simone Orsi <simone.orsi@camptocamp.com>
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import fields, models


class StorageBackend(models.Model):
    _inherit = "storage.backend"

    backend_type = fields.Selection(
        selection_add=[("webdav", "Webdav")], ondelete={"webdav": "set default"}
    )
    webdav_server = fields.Char(string="Webdav Host")
    webdav_login = fields.Char(
        string="Webdav Login", help="Login to connect to webdav server"
    )
    webdav_password = fields.Char(string="Webdav Password")

    @property
    def _server_env_fields(self):
        env_fields = super()._server_env_fields
        env_fields.update(
            {
                "webdav_password": {},
                "webdav_login": {},
                "webdav_server": {},
            }
        )
        return env_fields
