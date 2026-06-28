class ZScoreAnomalyDetector:
    def __init__(self, threshold: float = 3.0):
        self.threshold = threshold

    def detect(self, value: float, mean: float, stddev: float) -> tuple[bool, float]:
        if stddev == 0.0:
            return False, 0.0
        z_score = abs(value - mean) / stddev
        return z_score > self.threshold, z_score
