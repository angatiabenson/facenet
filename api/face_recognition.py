import face_recognition as fr
import numpy as np


def extract_face_metadata(image_path):
    # Load the image
    image = fr.load_image_file(image_path)

    # Detect faces in the image
    face_locations = fr.face_locations(image)

    # Extract face encodings
    face_encodings = fr.face_encodings(image, face_locations)
    face_encoding = ' '.join(map(str, face_encodings[0]))
    if len(face_locations) == 1:
        return face_encoding
    else:
        return None


def compare_faces(known_face_encodings, unknown_face_encoding):
    known_face_encoding = np.array([float(x)
                                   for x in known_face_encodings.split(' ')])
    unknown_face_encoding = np.array(
        [float(x) for x in unknown_face_encoding.split(' ')])
    return fr.compare_faces([known_face_encoding], unknown_face_encoding)[0]
