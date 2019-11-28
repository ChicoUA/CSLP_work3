import numpy as np
import cv2


class video_player:
    def __init__(self, filename, video_format):
        self.filename = filename
        self.video_format = video_format

    def play(self):
        cap = cv2.VideoCapture(self.filename)

        while cap.isOpened():
            ret, frame = cap.read()

            if self.video_format == "RGB":
                newframe = cv2.cvtColor(frame, cv2.COLOR_YUV2BGR)
            elif self.video_format == "YUV":
                newframe = cv2.cvtColor(frame, cv2.COLOR_BGR2YUV)
            elif self.video_format == "GRAY":
                newframe = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            elif self.video_format == "HSV":
                newframe = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
            else:
                newframe = frame

            cv2.imshow('frame', newframe)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        cap.release()
        cv2.destroyAllWindows()


def main():
    filename = "http://commondatastorage.googleapis.com/gtv-videos-bucket/sample/Sintel.mp4"
    vformat = "HSV"

    vp = video_player(filename, vformat)
    vp.play()


if __name__ == '__main__':
    main()
