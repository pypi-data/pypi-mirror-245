# Create aliases of sub modules from feature_store; They will be moved completely to feature_engineering in the future
import sys

from databricks.feature_store import online_store_publish_client, online_store_spec

sys.modules["databricks.feature_engineering.online_store_publish_client"] = sys.modules[
    "databricks.feature_store.online_store_publish_client"
]
sys.modules["databricks.feature_engineering.online_store_spec"] = sys.modules[
    "databricks.feature_store.online_store_spec"
]


# Inject FeatureEngineeringClient specific things
from databricks.feature_engineering.version import VERSION
from databricks.feature_store.utils import request_context
from databricks.feature_store.utils.logging_utils import (
    _configure_feature_store_loggers,
)
from databricks.feature_store.utils.request_context import RequestContext


def inject_fe_client_version_to_fs_client_request_context():
    divider = "+fe-client_"
    if divider not in request_context.VERSION:
        request_context.VERSION = request_context.VERSION + divider + VERSION


def inject_upgrade_workspace_table_request_method():
    request_context.UPGRADE_WORKSPACE_TABLE = "upgrade_workpace_table"
    if (
        request_context.UPGRADE_WORKSPACE_TABLE
        not in RequestContext.valid_feature_store_method_names
    ):
        RequestContext.valid_feature_store_method_names.append(
            request_context.UPGRADE_WORKSPACE_TABLE
        )


_configure_feature_store_loggers(root_module_name=__name__)
inject_fe_client_version_to_fs_client_request_context()
inject_upgrade_workspace_table_request_method()


# Support sugar-syntax `from databricks.feature_engineering import FeatureEngineeringClient`, etc.
from databricks.feature_engineering.client import FeatureEngineeringClient
from databricks.feature_engineering.decorators import feature_table
from databricks.feature_engineering.entities.feature_function import FeatureFunction
from databricks.feature_engineering.entities.feature_lookup import FeatureLookup
from databricks.feature_engineering.upgrade_client import UpgradeClient

__all__ = [
    "FeatureEngineeringClient",
    "feature_table",
    "FeatureLookup",
    "FeatureFunction",
    "UpgradeClient",
]
