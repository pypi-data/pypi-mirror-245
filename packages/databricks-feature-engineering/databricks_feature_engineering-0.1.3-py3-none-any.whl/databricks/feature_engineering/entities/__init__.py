# Create aliases of sub modules from feature_store; They will be moved completely to feature_engineering in the future
import sys

from databricks.feature_store.entities import (
    _feature_store_object,
    feature_function,
    feature_lookup,
    feature_table,
)

sys.modules["databricks.feature_engineering.entities.feature_function"] = sys.modules[
    "databricks.feature_store.entities.feature_function"
]
sys.modules["databricks.feature_engineering.entities.feature_lookup"] = sys.modules[
    "databricks.feature_store.entities.feature_lookup"
]
sys.modules["databricks.feature_engineering.entities.feature_table"] = sys.modules[
    "databricks.feature_store.entities.feature_table"
]
sys.modules[
    "databricks.feature_engineering.entities._feature_store_object"
] = sys.modules["databricks.feature_store.entities._feature_store_object"]

try:
    # The new classes are available in databricks-feature-store 0.15+ only
    from databricks.feature_store.entities import (
        feature_serving_endpoint,
        feature_spec_info,
    )

    sys.modules[
        "databricks.feature_engineering.entities.feature_serving_endpoint"
    ] = sys.modules["databricks.feature_store.entities.feature_serving_endpoint"]
    sys.modules[
        "databricks.feature_engineering.entities.feature_spec_info"
    ] = sys.modules["databricks.feature_store.entities.feature_spec_info"]
except ImportError:
    pass
