from flask import Flask, Response, jsonify
import cv2
from detection import detect_objects

app = Flask(__name__)
cap = cv2.VideoCapture(0)  # USB camera

@app.route('/video_feed')
def video_feed():
    def generate():
        while True:
            success, frame = cap.read()
            if not success:
                break
            frame, _ = detect_objects(frame)
            ret, buffer = cv2.imencode('.jpg', frame)
            frame_bytes = buffer.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')

    return Response(generate(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/detect')
def detect_once():
    success, frame = cap.read()
    if not success:
        return jsonify({'error': 'Camera read failed'})
    _, detections = detect_objects(frame)
    return jsonify({'detections': detections})

if __name__ == "__main__":
    app.run(debug=True)
