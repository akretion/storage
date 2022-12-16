# Copyright 2022 Akretion (https://www.akretion.com).
# @author Sébastien BEAU <sebastien.beau@akretion.com>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

import logging
import os

from odoo.addons.component.core import Component

_logger = logging.getLogger(__name__)

try:
    import fsspec
except ImportError as err:  # pragma: no cover
    _logger.debug(err)


class WebdavBackendAdapter(Component):
    _name = "webdav.adapter"
    _inherit = "base.storage.adapter"
    _usage = "webdav"

    def _get_client_params(self):
        backend = self.collection
        return {
            "base_url": backend.webdav_server,
            "auth": (backend.webdav_login, backend.webdav_password),
        }

    def _get_client(self):
        kwargs = self._get_client_params()
        return fsspec.get_filesystem_class(self.collection.backend_type)(**kwargs)

    def add(self, relative_path, data, **kwargs):
        kwargs = self._get_client_params()
        full_path = self._fullpath(relative_path)
        with fsspec.open(f"webdav://{full_path}", mode="w+b", **kwargs) as f:
            f.write(data)

    def get(self, relative_path, **kwargs):
        kwargs = self._get_client_params()
        full_path = self._fullpath(relative_path)
        with fsspec.open(f"webdav://{full_path}", mode="rb", **kwargs) as f:
            return f.read()

    def list(self, relative_path):
        client = self._get_client()
        full_path = self._fullpath(relative_path)
        return [
            x.replace(f"{full_path}/", "") for x in client.ls(full_path, detail=False)
        ]

    def move_files(self, files, destination_path):
        _logger.debug("mv %s %s", files, destination_path)
        client = self._get_client()
        for file_path in files:
            dest_file_path = os.path.join(destination_path, os.path.basename(file_path))
            client.mv(file_path, dest_file_path)

    def delete(self, relative_path):
        client = self._get_client()
        file_path = self._fullpath(relative_path)
        return client.rm_file(file_path)

    def validate_config(self):
        self.list("")
