import pickle
from sklearn.metrics import confusion_matrix, classification_report

def evaluate_model(model_path, X_test, y_test):
    # Load the model
    with open(model_path, 'rb') as f:
        model = pickle.load(f)

    # Predict
    y_pred = model.predict(X_test)

    # Define all possible labels
    labels = [0, 1]  # Replace with actual labels in your dataset

    # Compute metrics
    cm = confusion_matrix(y_test, y_pred, labels=labels)
    report = classification_report(y_test, y_pred, labels=labels, output_dict=True)

    metrics = {
        'accuracy': model.score(X_test, y_test),
        'confusion_matrix': cm.tolist(),
        'classification_report': report
    }

    return metrics