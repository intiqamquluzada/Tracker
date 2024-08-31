import yfinance as yf
import torch
import torch.nn as nn
import numpy as np
from sklearn.preprocessing import MinMaxScaler
from torch.utils.data import DataLoader, TensorDataset

import logging

logger = logging.getLogger(__name__)

def create_sequences(data, seq_length):
    xs, ys = [], []
    for i in range(len(data) - seq_length):
        x = data[i:i + seq_length]
        y = data[i + seq_length]
        xs.append(x)
        ys.append(y)
    return np.array(xs), np.array(ys)


def predicter(symbol, start_date, end_date):
    # Hyperparameters
    input_size = 1
    hidden_size = 64
    num_layers = 2
    num_epochs = 100
    default_sequence_length = 100  # Desired sequence length
    learning_rate = 0.001

    # Step 1: Download the cryptocurrency data from Yahoo Finance
    crypto_symbol = symbol  # Symbol
    data = yf.download(crypto_symbol, start=start_date, end=end_date)
    prices = data['Close'].values.astype(float)

    sequence_length = min(len(prices), default_sequence_length)

    if len(prices) < sequence_length:
        logger.warning(f"Not enough data to create sequences. Available data points: {len(prices)}, required: {sequence_length}")
        return None  # Handle the case where there isn't enough data

    # Step 2: Normalize the data
    scaler = MinMaxScaler(feature_range=(0, 1))
    prices_normalized = scaler.fit_transform(prices.reshape(-1, 1))

    # Step 3: Convert data to PyTorch tensors
    x_data, y_data = create_sequences(prices_normalized, sequence_length)

    if len(x_data) == 0:
        logger.warning("No sequences could be created from the data.")
        return None  # Handle the case where no sequences are created

    x_data = torch.tensor(x_data, dtype=torch.float32)
    y_data = torch.tensor(y_data, dtype=torch.float32)

    # Step 4: Create DataLoader
    dataset = TensorDataset(x_data, y_data)
    dataloader = DataLoader(dataset, batch_size=32, shuffle=True)

    # Step 5: Define the LSTM model
    class LSTMModel(nn.Module):
        def __init__(self, input_size, hidden_size, num_layers):
            super(LSTMModel, self).__init__()
            self.lstm = nn.LSTM(input_size, hidden_size, num_layers, batch_first=True)
            self.fc = nn.Linear(hidden_size, 1)

        def forward(self, x):
            h_0 = torch.zeros(num_layers, x.size(0), hidden_size).to(x.device)
            c_0 = torch.zeros(num_layers, x.size(0), hidden_size).to(x.device)
            output, (h_n, c_n) = self.lstm(x, (h_0, c_0))
            output = self.fc(output[:, -1, :])
            return output

    # Step 6: Initialize the model, loss function, and optimizer
    model = LSTMModel(input_size, hidden_size, num_layers)
    criterion = nn.MSELoss()
    optimizer = torch.optim.Adam(model.parameters(), lr=learning_rate)

    # Step 7: Training loop
    for epoch in range(num_epochs):
        for inputs, targets in dataloader:
            optimizer.zero_grad()
            outputs = model(inputs)
            loss = criterion(outputs, targets)
            loss.backward()
            optimizer.step()

        if (epoch + 1) % 10 == 0:
            print(f'Epoch [{epoch + 1}/{num_epochs}], Loss: {loss.item():.4f}')

    # Step 8: Save the model
    torch.save(model.state_dict(), 'crypto_predictor.pth')

    # Step 9: Predict the next price
    model.eval()
    with torch.no_grad():
        if len(prices_normalized) >= sequence_length:
            last_sequence = torch.tensor(prices_normalized[-sequence_length:], dtype=torch.float32).unsqueeze(0)
            next_price = model(last_sequence).item()
            next_price = scaler.inverse_transform(np.array(next_price).reshape(-1, 1))

            print(next_price[0][0])
            s = float("{:.2f}".format(float(next_price[0][0])))
            return s
        else:
            logger.warning("Not enough data for prediction.")
            return None



