# -*- coding: utf-8 -*-
# Time       : 2022/1/20 16:16
# Author     : QIN2DIM
# Github     : https://github.com/QIN2DIM
# Description:
import shutil
import sys
import webbrowser
from typing import Optional

from webdriver_manager.chrome import ChromeType
from webdriver_manager.utils import get_browser_version_from_os

from services.settings import DIR_MODEL, logger, DIR_ASSETS
from services.utils import YOLO, get_challenge_ctx, Rainbow, PluggableObjects


def download_driver():
    # Detect environment variable `google-chrome`.
    browser_version = get_browser_version_from_os(ChromeType.GOOGLE)
    if browser_version != "UNKNOWN":
        return

    # `google-chrome` is missing from environment variables, prompting players to install manually.
    logger.critical(
        "The current environment variable is missing `google-chrome`, "
        "please install Chrome for your system"
    )
    logger.info(
        "Ubuntu: https://linuxize.com/post/how-to-install-google-chrome-web-browser-on-ubuntu-20-04/"
    )
    logger.info(
        "CentOS 7/8: https://linuxize.com/post/how-to-install-google-chrome-web-browser-on-centos-7/"
    )
    if "linux" not in sys.platform:
        webbrowser.open("https://www.google.com/chrome/")

    logger.info("Re-execute the `install` scaffolding command after the installation is complete.")


def do(yolo_onnx_prefix: Optional[str] = None, upgrade: Optional[bool] = False):
    """下载项目运行所需的各项依赖"""
    dir_assets = DIR_ASSETS

    download_driver()

    if upgrade is True:
        logger.debug(f"Reloading the local cache of Assets {dir_assets}")
        shutil.rmtree(dir_assets, ignore_errors=True)
    Rainbow(dir_assets).sync(force=upgrade)
    PluggableObjects(dir_assets).sync()

    # PULL YOLO ONNX Model by the prefix flag
    YOLO(DIR_MODEL, yolo_onnx_prefix).pull_model()


@logger.catch()
def test():
    """Check if the Challenger driver version is compatible"""
    ctx = get_challenge_ctx(silence=True)
    try:
        ctx.get("https://blog.echosec.top/p/spider_performance/")
    finally:
        ctx.quit()

    logger.success("The adaptation is successful")
