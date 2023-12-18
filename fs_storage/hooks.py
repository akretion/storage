# Copyright 2023 Akretion
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
import logging

_logger = logging.getLogger(__name__)


def pre_init_hook(cr):
    _logger.info("AK hack: UPD columns to remove backend_id on attachment_synchronize")
    cr.execute(
        """
        UPDATE attachment_synchronize_task
        SET storage_id=null;
        """
    )
    _logger.info("AK hack end")
