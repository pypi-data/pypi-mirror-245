import pytest
import tensorflow as tf
import torch
import torch.nn as nn
import torch.nn.functional as F
from d_npu_alli import client


def test_parse_variables():
    model_str = "model1"
    train_loader_str = "train_loader2"
    test_loader_str = "test_loader3"
    user_fit = "fit4"
    user_evaluate = "evaluate5"
    line = f"""

client.run_federated_learning(
    model={model_str},
    train_loader={train_loader_str},
    test_loader={test_loader_str},
)
"""
    result = client._parse_variables(line)
    assert result == {
        "model": model_str,
        "train_loader": train_loader_str,
        "test_loader": test_loader_str,
    }

    line = f"""
client.run_federated_learning( model={model_str},
    train_loader={train_loader_str}, test_loader={test_loader_str},
    user_fit={user_fit},
    user_evaluate={user_evaluate}
)
"""
    result = client._parse_variables(line)
    assert result == {
        "model": model_str,
        "train_loader": train_loader_str,
        "test_loader": test_loader_str,
        "user_fit": user_fit,
        "user_evaluate": user_evaluate,
    }


def test_get_framework_name():
    tf_model = tf.keras.applications.MobileNetV2(
        (32, 32, 3), classes=10, weights=None
    )
    result = client._get_framework_name(tf_model)
    assert result == client.Model.TENSORFLOW

    torch_model = Net()
    result = client._get_framework_name(torch_model)
    assert result == client.Model.TORCH

    with pytest.raises(NotImplementedError):
        not_implemented = NotImplementedError()
        result = client._get_framework_name(not_implemented)


class Net(nn.Module):
    """Model (simple CNN adapted from 'PyTorch: A 60 Minute Blitz')"""

    def __init__(self) -> None:
        super(Net, self).__init__()
        self.conv1 = nn.Conv2d(3, 6, 5)
        self.pool = nn.MaxPool2d(2, 2)
        self.conv2 = nn.Conv2d(6, 16, 5)
        self.fc1 = nn.Linear(16 * 5 * 5, 120)
        self.fc2 = nn.Linear(120, 84)
        self.fc3 = nn.Linear(84, 10)

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        x = self.pool(F.relu(self.conv1(x)))
        x = self.pool(F.relu(self.conv2(x)))
        x = x.view(-1, 16 * 5 * 5)
        x = F.relu(self.fc1(x))
        x = F.relu(self.fc2(x))
        return self.fc3(x)


class NotImplemented:
    pass
