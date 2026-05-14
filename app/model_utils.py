"""
Model loading and prediction logic.

The model must be loaded ONCE at module level, NOT inside the predict function.
"""

# TODO 1: Load your serialized churn model from data/model.joblib
import pickle
import joblib
encoder=joblib.load('data/column_transformer.joblib')

with open('data/model.pkl', 'rb') as f:
    model = pickle.load(f)


def predict_churn(features: list) -> int:
    """
    Takes a list of feature values and returns a churn prediction (0 or 1).
    """
    # TODO 2: Use model.predict() to get a prediction and return it as an int
    #         Hint: model.predict() expects a 2D array
    # If features is already a 2D array (e.g. from encoder), just pass it
    if isinstance(features, list) and len(features) > 0 and isinstance(features[0], list):
        return int(model.predict(features)[0])
    return int(model.predict([features])[0])


if __name__ == "__main__":
    import pandas as pd
    # TODO 3: Replace with sample features that match your model
    sample_data = [[600, 'France', 'Male', 42, 2, 0, 1, 1, 1, 101348]]
    columns = ['CreditScore', 'Geography', 'Gender', 'Age', 'Tenure', 'Balance', 'NumOfProducts', 'HasCrCard', 'IsActiveMember', 'EstimatedSalary']
    sample_df = pd.DataFrame(sample_data, columns=columns)
    sample = encoder.transform(sample_df)
    # features_1d = sample[0].tolist()
    # print(f"Input:      {features_1d}")
    print(f"Prediction: {predict_churn(sample)}")
