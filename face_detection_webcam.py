from flask import Flask, render_template, Response
from multiprocessing import Queue
from threading import Thread
import cv2
import time
import thread
import sys

broadcast_list = []

def broadcast_frame():
    global broadcast_list
    print("broadcast frame")

    faceCascade = cv2.CascadeClassifier(sys.argv[1])

    video_capture = cv2.VideoCapture(0)
    video_capture.set(3, 600)
    video_capture.set(4, 800)

    while True:
        ret, frame = video_capture.read()

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        faces = faceCascade.detectMultiScale(
            gray,
            scaleFactor=1.1,
            minNeighbors=5,
            minSize=(30, 30),
            flags=cv2.cv.CV_HAAR_SCALE_IMAGE
        )

        # Draw a rectangle around the faces
        for (x, y, w, h) in faces:
            cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)

        ret, jpeg = cv2.imencode('.jpg', frame)
        client_num = len(broadcast_list)
        if client_num > 0:
            for client in range(0, client_num):
                try:
                    broadcast_list[client].put_nowait(jpeg.tostring())
                except:
                    print("send error, delete client")
                    del broadcast_list[client]

        time.sleep(.05)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    
    video_capture.release()
    cv2.destroyAllWindows()




app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

def gen():
    global broadcast_list
    frame_queue = Queue(1)
    broadcast_list.append(frame_queue)
    while True:
        try:
            frame = frame_queue.get()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')
        except ValueError:
            broadcast_list.remove(frame_queue)
            break

@app.route('/video_feed')
def video_feed():
    return Response(gen(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    webcam_daemon = Thread(target=broadcast_frame, args=())
    webcam_daemon.daemon = True
    webcam_daemon.start()

    print("start web")
    app.run(host='0.0.0.0', debug=True, threaded=True, use_reloader=False)

