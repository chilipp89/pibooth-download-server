# -*- coding: utf-8 -*-

"""Pibooth plugin to download picture via qr code."""

import pibooth
from pibooth.utils import LOGGER


__version__ = "0.1.2"

from qr_filetransfer import start_download_server

SECTION = 'DOWNLOAD_SERVER'


@pibooth.hookimpl
def pibooth_configure(cfg):
    """Declare the new configuration options"""
    cfg.add_option(SECTION, 'upload_available_seconds', 300,
                   "Duration the image is available")


@pibooth.hookimpl
def state_processing_exit(cfg, app):
    """
    Generate the QR Code and store it in the application.
    """

    LOGGER.info("Start Download Server ...")
    app.previous_picture_url = start_download_server(app.previous_picture_file,
                                                     auth=None,
                                                     duration=int(cfg.get(SECTION, 'upload_available_seconds')))
    LOGGER.info(f"Started Download Server for {cfg.get(SECTION, 'upload_available_seconds')} seconds")
