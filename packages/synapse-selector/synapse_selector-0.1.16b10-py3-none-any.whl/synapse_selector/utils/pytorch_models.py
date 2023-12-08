import torch
import numpy as np

from synapse_selector.utils.iglu_cnn import PeakDetectionModel_convout


class torch_cnn_model:
    def __init__(
        self,
        model_path: str = "./models/peak_detection-conv_output.pt",
        window_len: int = 50,
    ) -> None:
        model = PeakDetectionModel_convout()
        model.load_state_dict(torch.load(model_path))
        model.eval()

        self.model = model
        self.window_len = window_len
        self.to_pad = 0
        self.preds = []

    def predict(self, arr: np.ndarray, threshold: float = 0.5) -> list[int]:
        # reshape input to (1, 1, length)
        input_tensor = torch.reshape(
            torch.tensor(arr, dtype=torch.float), (1, 1, arr.shape[0])
        )
        self.preds = np.array(self.model(input_tensor).detach().flatten())
        infered_peaks = list(np.argwhere(self.preds > threshold).flatten())
        return infered_peaks

    def update_predictions(self, threshold: float) -> list[int]:
        infered_peaks = list(np.argwhere(self.preds > threshold).flatten())
        return infered_peaks
