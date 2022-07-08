import numpy as np
from extractors.wrappers.f0_dnn_wrapper import f0_dnn_wrapper

class DnnExtractor:
    @staticmethod
    def extract_as_hz(audio, sample_rate, hop_size, audio_filepath='', frame_size=1024):
        f0_processor = f0_dnn_wrapper()
        # We use window size == hop size until further testing to make sure behavior is correct otherwise
        f0_processor.configure(sample_rate, 480, 480)
        n_frames = np.ceil(len(audio) / 480)
        audio = np.array_split(audio, n_frames)
        f0_hz = np.zeros(int(n_frames))
        f0_confidence = np.zeros(int(n_frames))
        for i, chunk in enumerate(audio):
            f0, confidence = f0_processor.process(chunk, False)
            f0_hz[i] = f0
            f0_confidence[i] = confidence
        latency = int(f0_processor.totalLatency() // 480)
        f0_hz = np.pad(f0_hz, (0, latency))[latency:]
        f0_confidence = np.pad(f0_confidence, (0, latency))[latency:]

        return f0_hz, f0_confidence
