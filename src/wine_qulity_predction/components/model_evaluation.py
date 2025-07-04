import numpy as np
import pandas as pd
import mlflow
import joblib
from urllib.parse import urlparse
import mlflow.sklearn
from urllib.parse import urlparse
from sklearn.metrics import mean_absolute_error, root_mean_squared_error, mean_squared_error, r2_score
from src.wine_qulity_predction.config.configuration import ModelEvaluationConfig
from src.wine_qulity_predction.utils.common import read_yaml, create_directories,save_json
from pathlib import  Path



class ModelEvaluation:
    def __init__(self, config: ModelEvaluationConfig):
        self.config = config

    def eval_metrics(self, actual, pred):
        rmse = root_mean_squared_error(actual, pred)
        mae = mean_absolute_error(actual, pred)
        r2 = r2_score(actual, pred)
        return rmse, mae, r2

    def log_into_mlflow(self, ):
        test_data = pd.read_csv(self.config.test_data_path)
        model = joblib.load(self.config.model_path)

        test_x = test_data.drop([self.config.target_column], axis=1)
        test_y = test_data[self.config.target_column]

        mlflow.set_registry_uri(self.config.mlflow_uri)
        tracking_url_type_parse = urlparse(mlflow.get_tracking_uri()).scheme

        with mlflow.start_run():
            predicted_qualities = model.predict(test_x)
            (rmse, mae, r2) = self.eval_metrics(test_y, predicted_qualities)

            #saving metrics as local
            scores = {'rmse': rmse, 'mae': mae, 'r2': r2}
            save_json(path=Path(self.config.metric_file_name), data=scores)

            mlflow.log_params(self.config.all_params)
            mlflow.log_metric("rmse", rmse)
            mlflow.log_metric("mae", mae)
            mlflow.log_metric("r2", r2)

            #model registry does not work with file store
            if tracking_url_type_parse != 'file':
                mlflow.sklearn.log_model(
                sk_model=model,
                artifact_path="model",
                # Remove any newer parameters that might cause issues
            )



            else:
                mlflow.sklearn.log_model(sk_model=model, artifact_path="model")







