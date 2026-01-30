import math

# Medallion: Bronze | Mutation: 0% | HIVE: I
# 🎯 PORT-1-BRIDGE: 1 Euro Filter (Adaptive Signal Denoising)
# Reference: http://www.lifl.fr/~casiez/1euro/

class LowPassFilter:
    def __init__(self, alpha):
        self.__setAlpha(alpha)
        self.__y = None
        self.__s = None

    def __setAlpha(self, alpha):
        if alpha <= 0 or alpha > 1.0:
            raise ValueError("Alpha must be in (0, 1.0]")
        self.__alpha = alpha

    def __call__(self, value, timestamp, alpha=None):
        if alpha is not None:
            self.__setAlpha(alpha)
        if self.__y is None:
            self.__s = value
        else:
            self.__s = self.__alpha * value + (1.0 - self.__alpha) * self.__s
        self.__y = value
        return self.__s

    def last_value(self):
        return self.__s

class OneEuroFilter:
    """
    1 Euro Filter with user-tunable presets.
    Specifically tuned for MediaPipe index-tip coordinates.
    """

    PRESETS = {
        "smooth": {
            "min_cutoff": 0.5,
            "beta": 0.001,
            "d_cutoff": 1.0
        },
        "snappy": {
            "min_cutoff": 1.0,
            "beta": 0.05,
            "d_cutoff": 1.0
        }
    }

    def __init__(self, freq=30, preset="smooth", min_cutoff=None, beta=None, d_cutoff=None):
        self.__freq = freq

        # Load preset or individual overrides
        config = self.PRESETS.get(preset, self.PRESETS["smooth"])
        self.__min_cutoff = min_cutoff if min_cutoff is not None else config["min_cutoff"]
        self.__beta = beta if beta is not None else config["beta"]
        self.__d_cutoff = d_cutoff if d_cutoff is not None else config["d_cutoff"]

        self.__x_filter = LowPassFilter(self.__alpha(self.__min_cutoff))
        self.__dx_filter = LowPassFilter(self.__alpha(self.__d_cutoff))
        self.__last_time = None

    def __alpha(self, cutoff):
        te = 1.0 / self.__freq
        tau = 1.0 / (2 * math.pi * cutoff)
        return 1.0 / (1.0 + tau / te)

    def __call__(self, x, timestamp=None):
        if self.__last_time is not None and timestamp is not None:
            self.__freq = 1.0 / (timestamp - self.__last_time)
        self.__last_time = timestamp

        # Estimate derivative
        prev_x = self.__x_filter.last_value()
        dx = 0.0 if prev_x is None else (x - prev_x) * self.__freq
        edx = self.__dx_filter(dx, timestamp, alpha=self.__alpha(self.__d_cutoff))

        # Compute adaptive cutoff
        cutoff = self.__min_cutoff + self.__beta * abs(edx)
        return self.__x_filter(x, timestamp, alpha=self.__alpha(cutoff))

# P1_VALIDATOR_ID: OMEGA_FILTER_V10
