import tqdm
import torch
from src.utils.model import save_checkpoint

def train(model, optimizer, loss_fn, train_loader, valid_loader, epochs=5):
    train_losses = []
    valid_losses = []
    for epoch in range(epochs):
        model.train()
        train_loss = 0.0
        pbar = tqdm(train_loader, desc=f'Epoch {epoch}')
        for data in pbar:
            x, y = data

            optimizer.zero_grad()
            y_pred = model(x)

            loss = loss_fn(y_pred, y)
            loss.backward()
            optimizer.step()

            train_loss += loss.item()
            pbar.set_postfix({'Train Loss': train_loss / len(train_loader)})
            train_losses.append(train_loss / len(train_loader))

        model.eval()
        valid_loss = 0.0
        with torch.no_grad():
            for data in valid_loader:
                x, y = data
                y_pred = model(x)
                loss = loss_fn(y_pred, y)
                valid_loss += loss.item()
            valid_losses.append(valid_loss / len(valid_loader))

        print(
            f'Epoch {epoch}, Train Loss: {train_loss / len(train_loader)}, Valid Loss: {valid_loss / len(valid_loader)}')

        return train_losses, valid_losses

    save_checkpoint(model, optimizer, epoch, loss)
