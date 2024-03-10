from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from .models import UserData, FaceMetadata
from django.shortcuts import render, redirect
from django.core.files.storage import FileSystemStorage
from .face_recognition import extract_face_metadata, compare_faces
from django.conf import settings
import os


def display_search_results(request):
    user_id = request.session.pop('found_user_id', None)
    if user_id:
        user_data = UserData.objects.get(id=user_id)
        return render(request, 'agent/display_user_data.html', {'user_data': user_data})
    else:
        return redirect('home')


def upload_and_search(request):
    if request.method == 'POST' and request.FILES['image']:
        image = request.FILES['image']

        # Temporarily save the image
        fs = FileSystemStorage()
        filename = fs.save(image.name, image)
        image_path = fs.path(filename)

        # Extract face data from the uploaded image
        uploaded_face_data = extract_face_metadata(image_path)

        # Attempt to find a matching user
        user_data = None
        for face_metadata in FaceMetadata.objects.all():
            # Assuming the comparison logic
            if compare_faces(face_metadata.face_encoding, uploaded_face_data):
                user_data = face_metadata.user_data
                break

        # Clean up: delete the temporarily stored image
        os.remove(image_path)

        if user_data:
            request.session['found_user_id'] = user_data.id
            return redirect('search_results')
        else:
            # If no user is found, redirect and indicate user not found
            messages.error(request, "No matching user found.")
            return redirect('home')

    return redirect('home')


def user_data_list(request):
    if request.method == 'POST':
        name = request.POST['name']
        phone = request.POST['phone']
        age = request.POST['age']
        region = request.POST['region']
        image = request.FILES['image']

        # Process the image file
        fs = FileSystemStorage()
        filename = fs.save(image.name, image)
        image_url = fs.url(filename)

        # Getting the absolute filesystem path of the saved image
        image_abs_path = os.path.join(settings.MEDIA_ROOT, filename)
        face_data = extract_face_metadata(image_abs_path)

        if face_data is None:
            messages.error(
                request, "Invalid image. Your image must have only one clear face.")
        else:
            # Create UserData instance
            data = UserData.objects.create(
                name=name,
                phone=phone,
                age=age,
                region=region,
                image=image_url
            )

            FaceMetadata.objects.create(
                user_data=data,
                face_encoding=face_data
            )
        return redirect('home')

    user_data = UserData.objects.all()
    return render(request, 'agent/index.html', {'user_data': user_data})


def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            # Redirect to a home or another appropriate page
            return redirect('home')
    else:
        form = UserCreationForm()
    return render(request, 'registration/register.html', {'form': form})


def login_user(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, "Invalid username or password")
            return render(request, 'registration/login.html', {})
    else:
        return render(request, 'registration/login.html', {})
# Create your views here.
