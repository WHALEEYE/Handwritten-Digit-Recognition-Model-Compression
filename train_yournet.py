"""
Train LeNet5

Example:
python train_yournet5.py \
  --checkpoint-dir ./checkpoints/YourNet5/ \
  --epoch-end 10 \
  --device cpu
"""
import argparse
import os

import torch
from torch import nn
from torchvision import datasets, transforms

from eval.metrics import get_accuracy
from models.YourNet import YourNet

# --------------- Arguments ---------------

parser = argparse.ArgumentParser()

parser.add_argument('--checkpoint-dir', type=str, required=True)
parser.add_argument('--last-checkpoint', type=str, default=None)

parser.add_argument('--device', type=str, choices=['cpu', 'cuda'], default='cpu')
parser.add_argument('--batch-size', type=int, default=64)
parser.add_argument('--epoch-start', type=int, default=0)
parser.add_argument('--epoch-end', type=int, required=True)

args = parser.parse_args()


# --------------- Loading ---------------

def train(model, train_loader, test_loader, optimizer, loss_fn):
    for epoch in range(args.epoch_start, args.epoch_end):
        print(f"Epoch {epoch}\n-------------------------------")
        size = len(train_loader.dataset)
        model.train()
        for batch_idx, (X, y) in enumerate(train_loader):

            X, y = X.to(args.device), y.to(args.device)

            # Compute prediction error
            pred_y = model(X)
            loss = loss_fn(pred_y, y)

            # Backpropagation
            optimizer.zero_grad()
            loss.backward()
            optimizer.step()

            if batch_idx % 100 == 0:
                loss, current = loss.item(), batch_idx * len(X)
                print(f"loss: {loss:>7f}  [{current:>5d}/{size:>5d}]")

        accuracy = get_accuracy(model, test_loader, args.device)
        print("Accuracy: %.3f" % accuracy)
        if accuracy > 0.982:
            break

        torch.save(model.state_dict(), args.checkpoint_dir + f'epoch-{epoch}.pth')


if __name__ == '__main__':

    train_loader = torch.utils.data.DataLoader(
        datasets.MNIST(root='./data', train=True, download=False,
                       transform=transforms.Compose([
                           transforms.ToTensor(),
                           transforms.Normalize((0.1307,), (0.3081,))
                       ])),
        batch_size=args.batch_size, shuffle=True)

    test_loader = torch.utils.data.DataLoader(
        datasets.MNIST(root='./data', train=False,
                       transform=transforms.Compose([
                           transforms.ToTensor(),
                           transforms.Normalize((0.1307,), (0.3081,))
                       ])),
        batch_size=args.batch_size, shuffle=True)

    model = YourNet().to(device=args.device)

    if args.last_checkpoint is not None:
        model.load_state_dict(torch.load(args.last_checkpoint, map_location=args.device))

    optimizer = torch.optim.AdamW(model.parameters(), lr=0.0042)
    loss_fn = nn.CrossEntropyLoss()

    if not os.path.exists(args.checkpoint_dir):
        os.makedirs(args.checkpoint_dir)

    train(model, train_loader, test_loader, optimizer, loss_fn)
