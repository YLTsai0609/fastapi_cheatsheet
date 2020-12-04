'''
the stream response
https://fastapi.tiangolo.com/advanced/custom-response/#streamingresponse

'''

# import the necessary packages
from pyimagesearch.motion_detection import SingleMotionDetector
# from imutils.video import VideoStream
# from fastapi import FastAPI
# from flask import Response
# from flask import Flask
# from flask import render_template
import threading
import argparse
import datetime
import imutils
import time
import cv2
import numpy as np
import sys


def now():
    return datetime.datetime.now().strftime('%y_%m_%d_%H_%M')


def add_text_overlays(frame: np.ndarray, oritation: str = 'h',
                      **kwargs) -> None:
    # WHITE_RGB = (241, 232, 229)
    WHITE_BGR = (229, 232, 241)
    current_info = ''
    for text, info in kwargs.items():
        if text and info:
            if isinstance(info, (int, float, complex))\
                    and not isinstance(info, bool):
                # is number
                current_info += f'{text} {info:.1f}  '
            elif isinstance(info, str):
                current_info += f'{text} {info}  '
            else:
                # python object always have __str__ attribute
                current_info += f'{text} {info}  '
            current_info += '\n'
    if oritation == 'h':
        current_info = current_info.replace('\n', '')
        cv2.putText(frame, current_info,
                    org=(10, 30),
                    fontFace=cv2.FONT_HERSHEY_SIMPLEX,
                    fontScale=0.5,
                    color=WHITE_BGR,
                    thickness=2, lineType=2)
    else:
        y0, dy = 30, 20
        for i, line in enumerate(current_info.split('\n')):
            y = y0 + i * dy
            cv2.putText(frame, line, (10, y),
                        fontFace=cv2.FONT_HERSHEY_SIMPLEX,
                        fontScale=0.5,
                        color=WHITE_BGR,
                        thickness=2, lineType=2)


# initialize the output frame and a lock used to ensure thread-safe
# exchanges of the output frames (useful for multiple browsers/tabs
# are viewing tthe stream)
outputFrame = None
lock = threading.Lock()

# initialize a flask object
app = Flask(__name__)

# initialize the video stream and allow the camera sensor to
# warmup
# vs = VideoStream(usePiCamera=1).start()
vs = VideoStream(src=0)
W, H, FPS = 1280, 720, 30
vs.stream.stream.set(cv2.CAP_PROP_FRAME_WIDTH, W)
vs.stream.stream.set(cv2.CAP_PROP_FRAME_HEIGHT, H)

vs.start()
time.sleep(2.0)


@app.route("/")
def index():
        # return the rendered template
    return render_template("index.html")


def detect_motion(frameCount):
    # grab global references to the video stream, output frame, and
    # lock variables
    global vs, outputFrame, lock

    # initialize the motion detector and the total number of frames
    # read thus far
    md = SingleMotionDetector(accumWeight=0.1)
    total = 0
    try:
        # loop over frames from the video stream
        # read the next frame from the video stream, resize it,
        while True:
            # convert the frame to grayscale, and blur it
            start = time.time()
            frame = vs.read()

            # frame = imutils.resize(frame, width=400)
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            gray = cv2.GaussianBlur(gray, (7, 7), 0)

            # grab the current timestamp and draw it on the frame
            timestamp = datetime.datetime.now()
            cv2.putText(frame, timestamp.strftime(
                "%A %d %B %Y %I:%M:%S%p"), (10, frame.shape[0] - 10),
                cv2.FONT_HERSHEY_SIMPLEX, 0.35, (0, 0, 255), 1)

            # if the total number of frames has reached a sufficient
            # number to construct a reasonable background model, then
            # continue to process the frame
            if total > frameCount:
                # detect motion in the image
                motion = md.detect(gray)

                # cehck to see if motion was found in the frame
                if motion is not None:
                                                        # unpack the tuple and draw the box surrounding the
                                                        # "motion area" on the output frame
                    (thresh, (minX, minY, maxX, maxY)) = motion
                    cv2.rectangle(frame, (minX, minY), (maxX, maxY),
                                  (0, 0, 255), 2)

            # update the background model and increment the total number
            # of frames read thus far
            md.update(gray)
            total += 1

            fps = (1 / (time.time() - start))
            info = {'FPS': fps}
            add_text_overlays(frame, **info)
            # acquire the lock, set the output frame, and release the
            # lock
            with lock:
                outputFrame = frame.copy()

    except KeyboardInterrupt:
        # quit
        print('this is a leave message')
        sys.exit()


def generate():
    # grab global references to the output frame and lock variables
    global outputFrame, lock

    # loop over frames from the output stream
    while True:
        # wait until the lock is acquired
        with lock:
            # check if the output frame is available, otherwise skip
            # the iteration of the loop
            if outputFrame is None:
                continue

            # encode the frame in JPEG format
            (flag, encodedImage) = cv2.imencode(".jpg", outputFrame)

            # ensure the frame was successfully encoded
            if not flag:
                continue

        # yield the output frame in the byte format
        yield(b'--frame\r\n' b'Content-Type: image/jpeg\r\n\r\n' +
              bytearray(encodedImage) + b'\r\n')


@app.route("/video_feed")
def video_feed():
    # return the response generated along with the specific media
    # type (mime type)
    return Response(generate(),
                    mimetype="multipart/x-mixed-replace; boundary=frame")


# check to see if this is the main thread of execution
if __name__ == '__main__':
    # construct the argument parser and parse command line arguments
    ap = argparse.ArgumentParser()
    ap.add_argument("-i", "--ip", type=str, required=True,
                    help="ip address of the device")
    ap.add_argument("-o", "--port", type=int, required=True,
                    help="ephemeral port number of the server (1024 to 65535)")
    ap.add_argument("-f", "--frame-count", type=int, default=32,
                    help="# of frames used to construct the background model")
    args = vars(ap.parse_args())

    # start a thread that will perform motion detection
    t = threading.Thread(target=detect_motion, args=(
        args["frame_count"],))
    t.daemon = True
    t.start()

    # start the flask app
    app.run(host=args["ip"], port=args["port"], debug=True,
            threaded=True, use_reloader=False)

# release the video stream pointer
vs.stop()
