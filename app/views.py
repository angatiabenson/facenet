from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from .models import UserData, FaceMetadata
from django.shortcuts import render, redirect
from django.core.files.storage import FileSystemStorage
import face_rec as fr
from django.conf import settings
import os


@login_required
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

        # Create UserData instance
        data = UserData.objects.create(
            added_by=request.user,
            name=name,
            phone=phone,
            age=age,
            region=region,
            image=image_url
        )

        # Getting the absolute filesystem path of the saved image
        image_abs_path = os.path.join(settings.MEDIA_ROOT, filename)
        face_data = fr.extract_face_metadata(image_abs_path)

        FaceMetadata.objects.create(
            user=data,
            face_details=face_data
        )

        user_data = UserData.objects.filter(added_by=request.user)
        return render(request, 'agent/index.html', {'user_data': user_data})

    user_data = UserData.objects.filter(added_by=request.user)
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
