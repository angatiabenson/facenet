from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.core.files.storage import FileSystemStorage
import numpy as np  # Assuming you have numpy installed; if not, install it
# This is your custom function to generate metadata
from .face_recognition import extract_face_metadata, compare_faces


@api_view(['POST'])
def generate_face_metadata(request):
    if 'image' not in request.FILES or len(request.FILES) != 1:
        return Response({'message': 'Error occurred', 'error': 'Please upload exactly one image.'}, status=400)

    image = request.FILES['image']
    fs = FileSystemStorage()
    filename = fs.save(image.name, image)
    image_path = fs.path(filename)

    # This function should generate and return face metadata
    metadata = extract_face_metadata(image_path)

    fs.delete(filename)  # Delete the temporarily saved image

    if metadata is None:
        return Response({'message': 'Error occurred', 'error': 'No face metadata found on the image or image has more than one face.'}, status=404)

    return Response({'message': 'Face metadata generated', 'data': metadata})


@api_view(['POST'])
def compare_face_metadata(request):
    known_face = request.data.get('known_face')
    unknown_face = request.data.get('unknown_face')

    if not known_face or not unknown_face:
        return Response({'message': 'Error occurred', 'error': 'Please provide both metadata for known and unknown faces.'}, status=400)

    try:
        known_face_list = [float(num) for num in known_face.split(' ')]
        unknown_face_list = [float(num) for num in unknown_face.split(' ')]

        np.array(known_face_list)
        np.array(unknown_face_list)
    except ValueError:
        return Response({'message': 'Error occurred', 'error': 'Metadata should be a string of numbers separated by spaces " ".'}, status=400)

    # Assuming you have a function to compare these numpy arrays
    # Implement your comparison logic here
    are_similar = compare_faces(known_face, unknown_face)
    response_message = ""
    if are_similar:
        response_message = "positive"
    else:
        response_message = "negative"

    return Response({'message': 'Face metadata comparison results', 'data': response_message})
