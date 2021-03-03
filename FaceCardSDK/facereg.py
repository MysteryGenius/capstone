import face_recognition
import cv2
import numpy as np
import os, time

# Load images learn how to recognize them.
known_face_encodings = []
known_face_names = []
img_directory = "/FaceCardSDK/face_db/"

# # Refresh Known List on start
# for filename in os.listdir(img_directory):
#     # Get names of User Embedding
#     name = os.path.splitext(filename)[0].lower()

#     # Load Embedding from Text file
#     single_embed = np.loadtxt(img_directory+filename, dtype=float)

#     # Insert in array of known face encodings and their names
#     known_face_encodings.append(single_embed)
#     known_face_names.append(name)

# Enroll User: Pass in username, image will be read from facedb
def enrollUser(name, raw_image):
    # Update Embedding List
    image = face_recognition.load_image_file(raw_image)
    single_face_encoding = face_recognition.face_encodings(image)[0]
    print('encoding: ', single_face_encoding)
    if len(single_face_encoding) == 0:
        print("No Face Found")
        return False
    else:
        # Saving Embedding to Text file
        print("Saving Embedding")
        print("name: ", name)
        print(os.getcwd())
        os.chdir('..')
        print(os.getcwd())
        print("final path: ", os.getcwd() + img_directory)
        np.savetxt(os.getcwd() + img_directory + name.lower() + '.txt', single_face_encoding)
        print("Embedding Saved")
        return True

def verify(name, raw_image):
    known_face_encodings = []
    known_face_names = []
    face_names = []
    face_encoding = []

    # Take Current Frame For Verification
    image = face_recognition.load_image_file(raw_image)
    # Retrieve Encoding for Frame
    face_encoding = face_recognition.face_encodings(image)
    if len(face_encoding) == 0:
        print("Face Not Found")
        return False
    else: 
        face_encoding = face_encoding[0]

    # Load True Embedding from Text file
    print("Verify Directory: ",os.getcwd())
    single_embed = np.loadtxt(os.getcwd() + img_directory + name.lower()+'.txt', dtype=float)

    # Insert in array of known face encodings and their names
    known_face_encodings.append(single_embed)

    # Match the Embedding
    matches = face_recognition.compare_faces(known_face_encodings, face_encoding)

    for i in known_face_encodings: 
        matched_names = matchEmbedding(face_names, known_face_encodings, face_encoding)
    if name.lower() in matched_names:
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