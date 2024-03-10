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
        return Response({'message': 'Error occurred', 'error': 'No face metadata found oe image has more than one face.'}, status=404)

    return Response({'message': 'Face metadata generated', 'data': metadata})


@api_view(['POST'])
def compare_face_metadata(request):
    metadata1 = request.data.get('known_face')
    metadata2 = request.data.get('unknown_face')

    if not metadata1 or not metadata2:
        return Response({'message': 'Error occurred', 'error': 'Please provide both metadata for known and unknown faces.'}, status=400)

    try:
        metadata1_list = [float(num) for num in metadata1.split(' ')]
        metadata2_list = [float(num) for num in metadata2.split(' ')]
    except ValueError:
        return Response({'message': 'Error occurred', 'error': 'Metadata should be a string of numbers separated by spaces " ".'}, status=400)

    metadata1_array = np.array(metadata1_list)
    metadata2_array = np.array(metadata2_list)

    # Assuming you have a function to compare these numpy arrays
    # Implement your comparison logic here
    are_similar = compare_faces(metadata1_array, metadata2_array)
    response_message = ""
    if are_similar:
        response_message = "same"
    else:
        response_message = "not same"

    return Response({'message': 'Error occurred', 'data': response_message})
