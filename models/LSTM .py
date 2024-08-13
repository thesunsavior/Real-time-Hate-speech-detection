import torch


class LSTM(torch.nn.Module):
    def __init__(self, input_size, hidden_size, num_layers, num_classes, emb_matrix=None):
        super(LSTM, self).__init__()
        self.emb = torch.nn.Embedding(num_embeddings=len(vocab), embedding_dim=input_size,
                                      padding_idx=1, _weight=emb_matrix)
        self.hidden_size = hidden_size
        self.num_layers = num_layers
        self.lstm = torch.nn.LSTM(
            input_size, hidden_size, num_layers, batch_first=True, dropout=0.1)
        self.fc = torch.nn.Linear(hidden_size, num_classes)

    def forward(self, x):
        h0 = torch.zeros(self.num_layers, x.size(
            0), self.hidden_size).to(x.device)
        c0 = torch.zeros(self.num_layers, x.size(
            0), self.hidden_size).to(x.device)

        emb = self.emb(x)
        out, _ = self.lstm(emb, (h0, c0))
        out = self.fc(out[:, -1, :])
        return out
