import face_recognition


def extract_face_metadata(image_path):
    # Load the image
    image = face_recognition.load_image_file(image_path)

    # Detect faces in the image
    face_locations = face_recognition.face_locations(image)

    # Extract face encodings
    face_encodings = face_recognition.face_encodings(image, face_locations)
    face_encoding = ' '.join(map(str, face_encodings[0]))

    return face_encoding, face_locations


def compare_faces(known_face_encodings, unknown_face_encoding):
    known_face_encoding = known_face_encodings.split(' ')
    unknown_face_encoding = unknown_face_encoding.split(' ')
    return face_recognition.compare_faces([known_face_encoding], unknown_face_encoding)[0]
