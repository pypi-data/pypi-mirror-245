# Create an alias of Training Set from feature_store; It will be moved completely to feature_engineering in the future
from databricks.feature_store.training_set import TrainingSet

__all__ = ["TrainingSet"]
