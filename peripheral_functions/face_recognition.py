import cv2
import face_recognition
import pickle
import os

# Load or create face data
if os.path.exists("known_faces.pkl"):
    with open("known_faces.pkl", "rb") as f:
        known_faces = pickle.load(f)
else:
    known_faces = {"encodings": [], "names": []}


# Register new face function
def register_face(main_frame, user_name):
    rgb_main_frame = cv2.cvtColor(main_frame, cv2.COLOR_BGR2RGB)
    face_loc = face_recognition.face_locations(rgb_main_frame)
    if face_loc:
        face_encod = face_recognition.face_encodings(rgb_main_frame, face_loc)[0]
        known_faces["encodings"].append(face_encod)
        known_faces["names"].append(user_name)
        with open("known_faces.pkl", "wb") as fff:
            pickle.dump(known_faces, fff)
        print(f"Registered: {user_name}")
    else:
        print("No face found. Try again.")


# Webcam start
video = cv2.VideoCapture(0)

print("Press R to register a new face")
print("Press Q to quit")

# Variables for speed and persistent display
frame_counter = 0
detect_interval = 5
last_name = "Unknown"
last_face_location = None

while True:
    ret, frame = video.read()
    if not ret:
        break

    frame_counter += 1

    if frame_counter % detect_interval == 0:
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        face_locations = face_recognition.face_locations(rgb_frame)
        face_encodings = face_recognition.face_encodings(rgb_frame, face_locations)

        if face_encodings:
            face_encoding = face_encodings[0]
            face_location = face_locations[0]
            matches = face_recognition.compare_faces(known_faces["encodings"], face_encoding)
            face_distances = face_recognition.face_distance(known_faces["encodings"], face_encoding)

            name = "Unknown"
            if face_distances.any():
                best_match_index = face_distances.argmin()
                if matches[best_match_index]:
                    name = known_faces["names"][best_match_index]

            # Update cached values
            last_name = name
            last_face_location = face_location

    # Draw the latest face info even if not detected in this frame
    if last_face_location:
        top, right, bottom, left = last_face_location
        cv2.rectangle(frame, (left, top), (right, bottom), (100, 200, 250), 2)
        cv2.putText(frame, f"Hi, {last_name}", (left, top - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (50, 50, 255), 2)

    cv2.imshow("Iris Recognizer", frame)

    key = cv2.waitKey(1) & 0xFF
    if key == ord("r"):
        new_name = input("Enter your name: ")
        register_face(frame, new_name)
    elif key == ord("q"):
        break

video.release()
cv2.destroyAllWindows()
