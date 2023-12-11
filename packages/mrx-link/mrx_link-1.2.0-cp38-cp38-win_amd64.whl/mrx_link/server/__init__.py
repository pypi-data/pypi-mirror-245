#  MAKINAROCKS CONFIDENTIAL
#  ________________________
#
#  [2017] - [2021] MakinaRocks Co., Ltd.
#  All Rights Reserved.
#
#  NOTICE:  All information contained herein is, and remains
#  the property of MakinaRocks Co., Ltd. and its suppliers, if any.
#  The intellectual and technical concepts contained herein are
#  proprietary to MakinaRocks Co., Ltd. and its suppliers and may be
#  covered by U.S. and Foreign Patents, patents in process, and
#  are protected by trade secret or copyright law. Dissemination
#  of this information or reproduction of this material is
#  strictly forbidden unless prior written permission is obtained
#  from MakinaRocks Co., Ltd.
from jupyter_server.serverapp import ServerApp
from jupyter_server.utils import url_path_join
from mrx_link_core.common.info import APP_NAME

from mrx_link.common import KERNEL_ID_REGEX

from .handlers.cache import (
    CACHE_HANDLER_INFO,
    CacheExportHandler,
    CacheImportHandler,
    ClearCacheDirHandler,
)
from .handlers.dag_handler import DAGHandler
from .handlers.info import (
    CacheInfoHandler,
    ClosedInfoHandler,
    LicenseInfoHandler,
    MRXLinkInfoHandler,
    MRXRunwayInfoHandler,
    ServerAppInfoHandler,
)
from .handlers.license import (
    ActivateHandler,
    DeactivateHandler,
    IssueHandler,
    LicenseHandler,
    ShowActivationsHandler,
)
from .handlers.pipeline_export import (
    KfpPipelineExportHandler,
    MRXLinkPipelineExportHandler,
    MRXRunwayPipelineExportHandler,
    PyPipelineExportHandler,
)
from .handlers.pipeline_import import (
    KfpPipelineImportHandler,
    MRXLinkPipelineImportHandler,
)
from .handlers.update import NoticeInfoHandler, NoticeLatestHandler, UpdateHandler
from .handlers.ws_handler import MRXLinkWebSocketHandler
from .license.config import MRXLinkLicenseConfiguration, MRXLinkUpdateConfiguration


def setup_application(web_app: ServerApp) -> None:
    """setup whole handlers to web Application

    Args:
        web_app (ServerApp): Jupyter Server Application
    """
    # pylint: disable=too-many-locals

    MRXLinkLicenseConfiguration()
    MRXLinkUpdateConfiguration()

    # origin web_app.settings["serverapp"].max_body_size = 512 * 1024 * 1024 = 512MB
    # we can check this info on jupyter_server.serverapp.ServerApp
    if "serverapp" in web_app.settings:
        CACHE_HANDLER_INFO["cache_buffer_size"] = web_app.settings["serverapp"].max_body_size
        web_app.settings["serverapp"].max_body_size = 20 * web_app.settings["serverapp"].max_body_size

    host_pattern: str = ".*$"
    base_url = web_app.settings["base_url"]

    dag_route = url_path_join(base_url, APP_NAME, "dag", "kernels", KERNEL_ID_REGEX)
    ws_route = url_path_join(base_url, APP_NAME, "ws")

    kfp_pipeline_export_route = url_path_join(base_url, APP_NAME, "pipeline", "export")
    link_pipeline_export_route = url_path_join(base_url, APP_NAME, "link-pipeline", "export")
    py_pipeline_export_route = url_path_join(base_url, APP_NAME, "python", "export")
    runway_pipeline_export_route = url_path_join(base_url, APP_NAME, "runway", "pipeline", "export")

    kfp_pipeline_import_route = url_path_join(base_url, APP_NAME, "pipeline", "import")
    link_pipeline_import_route = url_path_join(base_url, APP_NAME, "link-pipeline", "import")

    cache_export_route = url_path_join(base_url, APP_NAME, "cache", "export")
    cache_import_route = url_path_join(base_url, APP_NAME, "cache", "import")
    cache_clear_route = url_path_join(base_url, APP_NAME, "cache", "clear")

    info_extension_route = url_path_join(base_url, APP_NAME, "info", "extension")
    info_serverapp_route = url_path_join(base_url, APP_NAME, "info", "serverapp")
    info_cache_route = url_path_join(base_url, APP_NAME, "info", "cache")
    info_license_route = url_path_join(base_url, APP_NAME, "info", "license")
    info_closed_route = url_path_join(base_url, APP_NAME, "info", "closed")
    info_runway_route = url_path_join(base_url, APP_NAME, "runway", "info")

    update_route = url_path_join(base_url, APP_NAME, "update")
    notice_route = url_path_join(base_url, APP_NAME, "notice")
    notice_latest_route = url_path_join(base_url, APP_NAME, "notice", "latest")

    license_route = url_path_join(base_url, APP_NAME, "license")
    register_route = url_path_join(base_url, APP_NAME, "license", "register")
    activation_route = url_path_join(base_url, APP_NAME, "license", "activation")
    deactivation_route = url_path_join(base_url, APP_NAME, "license", "deactivation")
    get_activations_route = url_path_join(base_url, APP_NAME, "license", "get_activations")

    handlers = [
        (dag_route, DAGHandler),
        (ws_route, MRXLinkWebSocketHandler),
        (kfp_pipeline_export_route, KfpPipelineExportHandler),
        (link_pipeline_export_route, MRXLinkPipelineExportHandler),
        (py_pipeline_export_route, PyPipelineExportHandler),
        (runway_pipeline_export_route, MRXRunwayPipelineExportHandler),
        (kfp_pipeline_import_route, KfpPipelineImportHandler),
        (link_pipeline_import_route, MRXLinkPipelineImportHandler),
        (cache_export_route, CacheExportHandler),
        (cache_import_route, CacheImportHandler),
        (cache_clear_route, ClearCacheDirHandler),
        (info_extension_route, MRXLinkInfoHandler),
        (info_serverapp_route, ServerAppInfoHandler),
        (info_cache_route, CacheInfoHandler),
        (info_license_route, LicenseInfoHandler),
        (info_closed_route, ClosedInfoHandler),
        (info_runway_route, MRXRunwayInfoHandler),
        (update_route, UpdateHandler),
        (notice_route, NoticeInfoHandler),
        (notice_latest_route, NoticeLatestHandler),
        (license_route, LicenseHandler),
        (register_route, IssueHandler),
        (activation_route, ActivateHandler),
        (deactivation_route, DeactivateHandler),
        (get_activations_route, ShowActivationsHandler),
    ]

    web_app.add_handlers(host_pattern, handlers)


__all__ = ["setup_application"]
