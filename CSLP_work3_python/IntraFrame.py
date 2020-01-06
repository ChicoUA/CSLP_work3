import numpy as np
from Golomb import *
from video_player import *
import sys

class IntraFrame:
    def __init__(self, moviename, outputfile, h, w, sampling):
        self.gol = Golomb(outputfile, 127)
        self.video = video_player(moviename, "RGB", sampling, h, w)
        self.frames = []
        self.count = 0
        self.decoded_frames = []

    def create_predictor(self, frame):
        predictor = []
        vs = []
        for i in range(self.video.height):
            for j in range(self.video.width):
                newvalue = 0
                value = int(frame.get_pixel(i, j, frame.Y))
                a = int(frame.get_pixel(i, j - 1, frame.Y))
                b = int(frame.get_pixel(i - 1, j, frame.Y))
                c = int(frame.get_pixel(i - 1, j - 1, frame.Y))

                if c >= max(a, b):
                    newvalue = value - min(a, b)
                elif c <= min(a, b):
                    newvalue = value - max(a, b)
                else:
                    newvalue = value - (a + b - c)

                predictor.append(newvalue + 255)

        for i in range(frame.U.shape[0]):
            for j in range(frame.U.shape[1]):

                newvalueu = 0
                value = int(frame.get_pixel(i, j, frame.U))
                a = int(frame.get_pixel(i, j - 1, frame.U))
                b = int(frame.get_pixel(i - 1, j, frame.U))
                c = int(frame.get_pixel(i - 1, j - 1, frame.U))
                if c >= max(a, b):
                    newvalueu = value - min(a, b)
                elif c <= min(a, b):
                    newvalueu = value - max(a, b)
                else:
                    newvalueu = value - (a + b - c)

                predictor.append(newvalueu + 255)

                newvaluev = 0
                value = int(frame.get_pixel(i, j, frame.V))
                a = int(frame.get_pixel(i, j - 1, frame.V))
                b = int(frame.get_pixel(i - 1, j, frame.V))
                c = int(frame.get_pixel(i - 1, j - 1, frame.V))
                if c >= max(a, b):
                    newvaluev = value - min(a, b)
                elif c <= min(a, b):
                    newvaluev = value - max(a, b)
                else:
                    newvaluev = value - (a + b - c)

                vs.append(newvaluev + 255)

        predictor += vs

        return predictor

    def get_frames(self):
        count = 0
        while True:
            count += 1
            ret, frame = self.video.read_raw()
            print(frame, count)
            if not ret:
                break
            self.frames.append(frame)

    def encode(self, frames):
        self.gol.bitstream.open_file_write()
        for frame in frames:
            pred = self.create_predictor(frame)
            self.count += 1
            print("count: ", self.count)

            for value in pred:
                self.gol.encode(value)

        if self.gol.bitstream.bitstream:
            self.gol.bitstream.padding_last_byte = 8 - len(self.gol.bitstream.bitstream)
            self.gol.bitstream.write_to_file()

        self.gol.bitstream.close_file()

    def decode(self):
        self.gol.bitstream.open_file_read()
        while self.count > 0:
            print(self.count)
            if self.video.sampling == "4:2:0":
                y = np.zeros([self.video.height, self.video.width])
                u = np.zeros([self.video.height // 2, self.video.width // 2])
                v = np.zeros([self.video.height // 2, self.video.width // 2])
                yuv = YUVFrame(self.video.sampling, y, u, v, self.video.height, self.video.width)

            elif self.video.sampling == "4:2:2":
                y = np.zeros([self.video.height, self.video.width])
                u = np.zeros([self.video.height, self.video.width // 2])
                v = np.zeros([self.video.height, self.video.width // 2])
                yuv = YUVFrame(self.video.sampling, y, u, v, self.video.height, self.video.width)

            else:
                y = np.zeros([self.video.height, self.video.width])
                u = np.zeros([self.video.height, self.video.width])
                v = np.zeros([self.video.height, self.video.width])
                yuv = YUVFrame(self.video.sampling, y, u, v, self.video.height, self.video.width)

            self.count -= 1

            for i in range(self.video.height):
                for j in range(self.video.width):
                    value = self.gol.decode() - 255
                    a = int(yuv.get_pixel(i, j - 1, yuv.Y))
                    b = int(yuv.get_pixel(i - 1, j, yuv.Y))
                    c = int(yuv.get_pixel(i - 1, j - 1, yuv.Y))

                    if c >= max(a, b):
                        newvalue = value + min(a, b)
                    elif c <= min(a, b):
                        newvalue = value + max(a, b)
                    else:
                        newvalue = value + (a + b - c)
                    yuv.Y[i][j] = newvalue

            for i in range(yuv.U.shape[0]):
                for j in range(yuv.U.shape[1]):
                    value = self.gol.decode() - 255
                    a = int(yuv.get_pixel(i, j - 1, yuv.U))
                    b = int(yuv.get_pixel(i - 1, j, yuv.U))
                    c = int(yuv.get_pixel(i - 1, j - 1, yuv.U))

                    if c >= max(a, b):
                        newvalue = value + min(a, b)
                    elif c <= min(a, b):
                        newvalue = value + max(a, b)
                    else:
                        newvalue = value + (a + b - c)

                    yuv.U[i][j] = newvalue

            for i in range(yuv.V.shape[0]):
                for j in range(yuv.V.shape[1]):
                    value = self.gol.decode() - 255
                    a = int(yuv.get_pixel(i, j - 1, yuv.V))
                    b = int(yuv.get_pixel(i - 1, j, yuv.V))
                    c = int(yuv.get_pixel(i - 1, j - 1, yuv.V))

                    if c >= max(a, b):
                        newvalue = value + min(a, b)
                    elif c <= min(a, b):
                        newvalue = value + max(a, b)
                    else:
                        newvalue = value + (a + b - c)

                    yuv.V[i][j] = newvalue

            self.decoded_frames.append(yuv)

        self.gol.bitstream.open_file_read()


def main():
    it = IntraFrame(sys.argv[1], "outputfile.txt", int(sys.argv[2]), int(sys.argv[3]), sys.argv[4])
    it.get_frames()
    it.encode(it.frames)
    it.decode()
    it.video.play2(it.decoded_frames)


if __name__ == '__main__':
    main()
