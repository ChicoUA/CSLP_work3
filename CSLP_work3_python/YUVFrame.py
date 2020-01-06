import numpy as np


class YUVFrame:
    def __init__(self, type, Y, U, V, height, width):
        self.Y = Y.copy()
        self.U = U.copy()
        self.V = V.copy()

        self.type = type
        self.h = height
        self.w = width

    def get_pixel(self, h, w, frame):
        if h < 0 or w < 0 or h >= frame.shape[0] or w >= frame.shape[1]:
            return 0

        value = frame[h][w]
        return value
