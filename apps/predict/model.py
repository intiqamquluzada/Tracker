import torch
import torch.nn as nn


# Define your model class (update this according to your model's architecture)
class CryptoPricePredictor(nn.Module):
    def __init__(self):
        super(CryptoPricePredictor, self).__init__()
        # Define your model layers here
        self.fc1 = nn.Linear(10, 64)  # Input layer with 10 features, output layer with 64 neurons
        self.fc2 = nn.Linear(64, 32)  # Hidden layer with 32 neurons
        self.fc3 = nn.Linear(32, 1)  # Output layer with 1 neuron (for single price prediction)
        self.relu = nn.ReLU()  # Activation function

    def forward(self, x):
        # Define the forward pass
        x = self.relu(self.fc1(x))  # Apply first layer and ReLU activation
        x = self.relu(self.fc2(x))  # Apply second layer and ReLU activation
        x = self.fc3(x)  # Apply output layer
        return x


def load_model():
    model_path = './model.pth'
    model = CryptoPricePredictor()
    model.load_state_dict(torch.load(model_path))
    model.eval()
    return model


def predict_stock_price(model, features):
    with torch.no_grad():
        inputs = torch.tensor(features, dtype=torch.float32)
        prediction = model(inputs)
        return prediction.item()
