# import torch
# from config.predicter import LSTMModel
#
# def load_model():
#     input_size = 1
#     hidden_size = 64
#     num_layers = 2
#
#     model = LSTMModel(input_size, hidden_size, num_layers)
#     model.load_state_dict(torch.load('crypto_predictor.pth'))
#     model.eval()  # Set the model to evaluation mode
#     return model