import face_recognition as fr
import numpy as np
import os
import cv2
import json


def encode_faces():
    encoded_data = {}

    for dirpath, dnames, fnames in os.walk("./Images"):
        for f in fnames:
            if f.endswith(".jpg") or f.endswith(".png"):
                face = fr.load_image_file("Images/" + f)
                encoding = fr.face_encodings(face)[0]
                encoded_data[f.split(".")[0]] = encoding

    # return encoded data of images
    return encoded_data

def detect_faces():
    with open("users.json", "r") as f: 
        users = json.load(f)
    faces = encode_faces()
    encoded_faces = list(faces.values())
    faces_name = list(faces.keys())

    video_frame = True
    # Capturing video through the WebCam
    # Real Time Video Streams
    video = cv2.VideoCapture(0)
    while True:
        ret, frame = video.read()

        if video_frame:
            face_locations = fr.face_locations(frame)
            unknown_face_encodings = fr.face_encodings(frame, face_locations)

            face_names = []
            for face_encoding in unknown_face_encodings:
                # Comapring faces
                matches = fr.compare_faces(encoded_faces, face_encoding)
                name = "Unknown"

                face_distances = fr.face_distance(encoded_faces, face_encoding)
                best_match_index = np.argmin(face_distances)
                if matches[best_match_index]:
                    name = faces_name[best_match_index]

                face_names.append(name)
                if name in users:
                    cv2.destroyAllWindows()
                    return name

        cv2.imshow('Video', frame)
        
        code = cv2.waitKey(1)
        # Press 'q' for close the video frame
        if code == ord('q'):
            break
        

    cv2.destroyAllWindows()

if __name__ == "__main__":
    detect_faces()