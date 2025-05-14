import pickle
from sklearn.ensemble import RandomForestClassifier

def train_and_save_model(X_train, y_train, model_path):
    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)
    
    # Open the file in write-binary mode and save the model
    with open(model_path, 'wb') as f:
        pickle.dump(model, f)
    
    print(f"✅ Model saved to {model_path}")