# Create an alias of feature_table from feature_store; It will be moved completely to feature_engineering in the future
from databricks.feature_store.decorators import feature_table

__all__ = ["feature_table"]
