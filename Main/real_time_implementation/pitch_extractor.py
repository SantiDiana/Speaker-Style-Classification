import numpy as np
import time
import csv
from extractors.dnn_extractor import DnnExtractor


class Methods:
    DNN     = 'DNN'


mapping = {
    Methods.DNN   : DnnExtractor,
}

class PitchExtractor:
    @staticmethod
    def extract_as_hz(audio, sample_rate, hop_size, method=Methods.DNN, audio_filepath='', frame_size=1024):
        extractor = mapping[method]

        start = time.time()
        print(hop_size)
        f0, conf = extractor.extract_as_hz(audio, sample_rate, hop_size, audio_filepath, frame_size)
        end = time.time()
        timer = end - start
        
        f0 = f0.astype(np.float32)
        f0 = np.nan_to_num(f0)
        
        if conf is None:
            conf = np.full(len(f0), 1.0)
        conf = conf.astype(np.float32)

        return f0, conf, timer
        
    @staticmethod
    def log_pitch(pitch_hz, confidence, times, pitch_file_path):
        with open(pitch_file_path, "w") as csvfile:
            writer = csv.writer(csvfile, delimiter=',')
            for i in range(len(pitch_hz)):
                writer.writerow([times[i], pitch_hz[i], confidence[i]])