import numpy as np
import cv2
from YUVFrame import *

class video_player:
    def __init__(self, filename, video_format, sampling, height, width):
        self.file = open(filename, "rb")
        self.video_format = video_format
        self.sampling = sampling
        self.height = height
        self.width = width
        self.fwidth = (width + 31) // 32 * 32
        self.fheight = (height + 15) // 16 * 16

    def read_raw(self):
        try:
            Y = 0
            U = 0
            V = 0
            mystery_value = 0
            if self.sampling == "4:4:4":
                mystery_value = 3
                stream = self.file.read(int(self.height * self.width * mystery_value))

                # Load the Y (luminance) data from the stream
                Y = np.fromfile(self.file, dtype=np.uint8, count=self.fwidth * self.fheight). \
                    reshape((self.fheight, self.fwidth))
                # Load the UV (chrominance) data from the stream, and double its size
                U = np.fromfile(self.file, dtype=np.uint8, count=self.fwidth * self.fheight). \
                    reshape((self.fheight, self.fwidth))

                V = np.fromfile(self.file, dtype=np.uint8, count=self.fwidth * self.fheight). \
                    reshape((self.fheight, self.fwidth))
            elif self.sampling == "4:2:2":
                mystery_value = 2
                stream = self.file.read(int(self.height * self.width * mystery_value))

                # Load the Y (luminance) data from the stream
                Y = np.fromfile(self.file, dtype=np.uint8, count=self.fwidth * self.fheight). \
                    reshape((self.fheight, self.fwidth))
                # Load the UV (chrominance) data from the stream, and double its size
                U = np.fromfile(self.file, dtype=np.uint8, count=(self.fwidth // 2) * self.fheight). \
                    reshape((self.fheight, self.fwidth // 2))

                V = np.fromfile(self.file, dtype=np.uint8, count=(self.fwidth // 2) * self.fheight). \
                    reshape((self.fheight, self.fwidth // 2))

            elif self.sampling == "4:2:0":
                mystery_value = 1.5
                stream = self.file.read(int(self.height * self.width * mystery_value))

                # Load the Y (luminance) data from the stream
                Y = np.fromfile(self.file, dtype=np.uint8, count=self.fwidth * self.fheight). \
                    reshape((self.fheight, self.fwidth))
                # Load the UV (chrominance) data from the stream, and double its size
                U = np.fromfile(self.file, dtype=np.uint8, count=(self.fwidth // 2) * (self.fheight // 2)). \
                    reshape((self.fheight // 2, self.fwidth // 2))

                V = np.fromfile(self.file, dtype=np.uint8, count=(self.fwidth // 2) * (self.fheight // 2)). \
                    reshape((self.fheight // 2, self.fwidth // 2))
            else:
                print("Wrong sampling")
                exit(1)

            yuv_frame = YUVFrame(self.sampling, Y, U, V, self.height, self.width)

            return True, yuv_frame
        except Exception:
            return False, []

    def read(self):
        ret, yuv = self.read_raw()
        if not ret:
            return ret, yuv
        BGR = self.convert_to_RGB(yuv)

        return ret, BGR

    def convert_to_RGB(self, yuv):
        # Stack the YUV channels together, crop the actual resolution, convert to
        # floating point for later calculations, and apply the standard biases
        YUV = None
        if self.sampling == "4:2:0":
            YUV = np.dstack((yuv.Y, yuv.U.repeat(2, axis=0).repeat(2, axis=1), yuv.V.repeat(2, axis=0).repeat(2, axis=1)))[:self.height, :self.width, :].astype(np.float)
        elif self.sampling == "4:2:2":
            YUV = np.dstack((yuv.Y, yuv.U.repeat(2, axis=1), yuv.V.repeat(2, axis=1)))[:self.height, :self.width, :].astype(np.float)
        else:
            YUV = np.dstack((yuv.Y, yuv.U, yuv.V))[:self.height, :self.width, :].astype(np.float)

        YUV[:, :, 0] = YUV[:, :, 0] - 16  # Offset Y by 16
        YUV[:, :, 1:] = YUV[:, :, 1:] - 128  # Offset UV by 128
        # YUV conversion matrix from ITU-R BT.601 version (SDTV)
        # Note the swapped R and B planes!
        #              Y       U       V
        M = np.array([[1.164, 2.017, 0.000],  # B
                      [1.164, -0.392, -0.813],  # G
                      [1.164, 0.000, 1.596]])  # R
        # Take the dot product with the matrix to produce BGR output, clamp the
        # results to byte range and convert to bytes
        BGR = YUV.dot(M.T).clip(0, 255).astype(np.uint8)
        return BGR

    def play(self):
        while True:
            ret, frame = self.read()
            if ret:
                cv2.imshow("frame", frame)

                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break
            else:
                break

    def play2(self, frames):
        for frame in frames:
            BGR = self.convert_to_RGB(frame)
            cv2.imshow("frame", BGR)

            if cv2.waitKey(30) & 0xFF == ord('q'):
                break


def main():
    filename = "tree_small.yuv"
    vformat = "RGB"

    vp = video_player(filename, vformat, "4:2:0", 288, 352)
    vp.play()


if __name__ == '__main__':
    main()
