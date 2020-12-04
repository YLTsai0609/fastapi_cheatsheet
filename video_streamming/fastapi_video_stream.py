'''
the stream response
https://fastapi.tiangolo.com/advanced/custom-response/#streamingresponse

currently (2020, Dec, 2) very few poeple to discuss how to implement video streamming server using fastapi, check issue

https://github.com/tiangolo/fastapi/issues?q=is%3Aissue+video+stream

So just back to use flask, waiting for more community support using fastapi

'''
import cv2
import numpy as np
import uvicorn
from fastapi import FastAPI
from fastapi.responses import StreamingResponse


app = FastAPI()
video = cv2.VideoCapture('movie_trailer.mp4')


def get_video_stream():
    global video
    while True:
        has_frame, frame = video.read()
        if not has_frame:
            break

        # (flag, encodedImage) = cv2.imencode(".jpg", frame)

        # if not flag:
        #     continue

        yield frame.tobytes()
        # yield(b'--frame\r\n' b'Content-Type: image/jpeg\r\n\r\n' +
        #       bytearray(encodedImage) + b'\r\n')


@app.get("/")
def root():
    a = "a"
    b = "b" + a
    return {"hello world": b}


# @app.get('/video_feed')
# def video_feed():
#     return StreamingResponse(get_video_stream(), media_type='multipart/x-mixed-replace')


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
