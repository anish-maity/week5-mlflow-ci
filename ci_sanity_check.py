import os
import mlflow
import pandas as pd
from sklearn import metrics
#demo


MLFLOW_TRACKING_URI = "http://35.232.105.223:8100/" #  MLflow URI
MODEL_NAME_REGISTRY = "iris-classifier-dt"
MODEL_STAGE = "Production"
MIN_ACCEPTABLE_ACCURACY = 0.90 # Set  minimum quality threshold


data = {
    'sepal_length': [5.1, 7.0, 6.3],
    'sepal_width': [3.5, 3.2, 3.3],
    'petal_length': [1.4, 4.7, 6.0],
    'petal_width': [0.2, 1.4, 2.5],
    'species': ['setosa', 'versicolor', 'virginica']
}
sanity_df = pd.DataFrame(data)

X_sanity = sanity_df[['sepal_length', 'sepal_width', 'petal_length', 'petal_width']]
y_sanity = sanity_df.species

# --- Sanity Check Function ---
def run_model_sanity_check():
    try:
        # 1. Set Tracking URI
        mlflow.set_tracking_uri(MLFLOW_TRACKING_URI)

        # 2. Load Production Model
        logged_model_uri = f"models:/{MODEL_NAME_REGISTRY}/{MODEL_STAGE}"
        loaded_model = mlflow.sklearn.load_model(logged_model_uri)
        print(f" Successfully loaded model from URI: {logged_model_uri}")

        # 3. Run Prediction and Evaluate
        prediction = loaded_model.predict(X_sanity)
        accuracy = metrics.accuracy_score(y_sanity, prediction)

        print(f"Sanity Check Model Accuracy: {accuracy:.4f}")

        # 4. Assert Sanity Check (the core CI gate)
        if accuracy >= MIN_ACCEPTABLE_ACCURACY:
            print(f"PASS: Accuracy {accuracy:.4f} >= Threshold {MIN_ACCEPTABLE_ACCURACY}. Model is safe.")
            return 0 # Success exit code
        else:
            print(f"FAIL: Accuracy {accuracy:.4f} < Threshold {MIN_ACCEPTABLE_ACCURACY}. Model quality failed sanity check.")
            return 1 # Failure exit code

    except Exception as e:
        print(f"FATAL CI ERROR: Could not complete sanity check. Error: {e}")
        # Return 1 for failure in the pipeline
        return 1

if __name__ == "__main__":
    exit_code = run_model_sanity_check()
    exit(exit_code)