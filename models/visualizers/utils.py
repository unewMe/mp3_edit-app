import numpy as np


def convert_to_librosa_format(array_of_samples: np.ndarray, channels: int, frame_rate: int) -> tuple[np.ndarray, int]:
    """Converts AudioSegment to librosa format (numpy array and sample rate)"""

    # Convert AudioSegment to numpy array
    samples = np.array(array_of_samples)
    if channels == 2:
        samples = samples.reshape((-1, 2)).mean(axis=1)  # Convert stereo to mono
    y = samples.astype(np.float32)

    # Normalize to [-1, 1] range if needed
    if np.issubdtype(samples.dtype, np.integer):
        y /= np.iinfo(samples.dtype).max

    sr = frame_rate
    return y, sr
