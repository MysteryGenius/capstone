import face_recognition
import cv2
import numpy as np
import os, time

# Load images learn how to recognize them.
known_face_encodings = []
known_face_names = []
img_directory = "./FaceCardSDK/face_db"

# Refresh Known List on start
for filename in os.listdir(img_directory):
    # Get names of User Embedding
    name = os.path.splitext(filename)[0].lower()

    # Load Embedding from Text file
    single_embed = np.loadtxt(filename, dtype=float)

    # Insert in array of known face encodings and their names
    known_face_encodings.append(single_embed)
    known_face_names.append(name)

# Enroll User: Pass in username, image will be read from facedb (Remove temp Image after this method)
def enrollUser(name, image):
    # Update Embedding List
    directory = "./FaceCardSDK/face_db"
    os.rename(image, name + '.jpg')
    image = face_recognition.load_image_file(name + '.jpg')
    single_face_encoding = face_recognition.face_encodings(image)[0]
    # Saving Embedding to Text file
    np.savetxt(name + '.txt', single_face_encoding)
    # Add Single Encoding to Known List
    known_face_encodings.append(single_face_encoding)
    known_face_names.append(name)
    return known_face_encodings, known_face_names

def verify(name, image):
    face_names = []
    face_encoding = []

    while len(face_encoding) == 0:
        # Take Current Frame
        image = face_recognition.load_image_file(directory + image)
        # Retrieve Encoding for Frame
        face_encoding = face_recognition.face_encodings(image)
        if len(face_encoding) != 0:
            face_encoding = face_encoding[0]
            break
    # Match the Embedding
    for i in known_face_encodings: 
        matched_names = matchEmbedding(face_names, known_face_encodings, face_encoding)
        if (len(matched_names) > 0 and matched_names.includes(name)):
            return True
        else:
            return False

def matchEmbedding(face_names, known_face_encodings, face_encoding):  
    name = "Unknown"
    # See if the face is a match for the known faces
    matches = face_recognition.compare_faces(known_face_encodings, face_encoding)

    # Or instead, use the known face with the smallest distance to the new face
    face_distances = face_recognition.face_distance(known_face_encodings, face_encoding)
    best_match_index = np.argmin(face_distances)
    if matches[best_match_index]:
        name = known_face_names[best_match_index]

    face_names.append(name)
    return face_names

# For Video Demonstration (Currently not in use)
def facereg(frame):

    # Initialize some variables
    face_locations = []
    face_encodings = []
    face_names = []
    process_this_frame = True

    # Resize frame of video to 1/4 size for faster face recognition processing
    small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)

    # Convert the image from BGR color (which OpenCV uses) to RGB color (which face_recognition uses)
    rgb_small_frame = small_frame[:, :, ::-1]

    # Only process every other frame of video to save time
    if process_this_frame:

        face_names = []
        # Find all the faces and face encodings in the current frame of video
        face_locations = face_recognition.face_locations(rgb_small_frame)
        face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)

        for face_encoding in face_encodings:
            matchEmbedding(face_names, known_face_encodings, face_encoding)

    process_this_frame = not process_this_frame
    # drawBoxes(frame, face_locations, face_names)

    return frame

# Drawing of Bounding Boxes (For demonstration purposes, currently not in use)
def drawBoxes(frame, face_locations, face_names):
    # Display the results
    for (top, right, bottom, left), name in zip(face_locations, face_names):
        # Scale back up face locations since the frame we detected in was scaled to 1/4 size
        top *= 4
        right *= 4
        bottom *= 4
        left *= 4

        # Draw a box around the face
        cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)

        # Draw a label with a name below the face
        cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED)
        font = cv2.FONT_HERSHEY_DUPLEX
        cv2.putText(frame, name, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)
    return frame