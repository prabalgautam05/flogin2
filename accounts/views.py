from django.shortcuts import render
import base64
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.files.base import ContentFile
from .models import UserImage
from django.contrib.auth.models import User
from django.db import IntegrityError
import face_recognition
import cv2
import numpy as np
import logging

# Configure logging
logger = logging.getLogger(__name__)

@csrf_exempt
def register(request):
    if request.method == 'POST':
        try:
            username = request.POST.get('username')
            face_image_data = request.POST.get('face_image')
            face_image_data = face_image_data.split(',')[1]
            face_image = ContentFile(base64.b64decode(face_image_data), name=f'{username}_.jpg')

            user = User.objects.create(username=username)
            UserImage.objects.create(user=user, face_image=face_image)

            return JsonResponse({'status': 'success', 'message': 'User registered successfully'})
        except IntegrityError:
            return JsonResponse({'status': 'error', 'message': 'Username already exists'})
        except Exception as e:
            logger.error(f"Error during registration: {e}")
            return JsonResponse({'status': 'error', 'message': str(e)})
    return render(request, 'register.html')

@csrf_exempt
def login_user(request):
    if request.method == "POST":
        username = request.POST.get('username')
        face_image_data = request.POST.get('face_image')

        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'User does not exist'}) 
        
        face_image_data = face_image_data.split(',')[1] 
        uploaded_image = ContentFile(base64.b64decode(face_image_data), name=f'{username}_.jpg')

        try:
            # Load the uploaded image using OpenCV
            nparr = np.frombuffer(uploaded_image.read(), np.uint8)
            uploaded_face_image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

            # Convert the image to RGB (face_recognition expects RGB images)
            uploaded_face_image = cv2.cvtColor(uploaded_face_image, cv2.COLOR_BGR2RGB)

            # Log the dimensions of the uploaded image
            logger.info(f"Uploaded image dimensions: {uploaded_face_image.shape}")

            # Get face encodings
            uploaded_face_encodings = face_recognition.face_encodings(uploaded_face_image)

            if uploaded_face_encodings:
                uploaded_face_encoding = uploaded_face_encodings[0]
                user_image = UserImage.objects.filter(user=user).last()

                # Log the path of the stored image
                logger.info(f"Stored image path: {user_image.face_image.path}")

                # Load the stored image using OpenCV
                stored_face_image = cv2.imread(user_image.face_image.path)

                # Check if the image was loaded correctly
                if stored_face_image is None:
                    logger.error("Failed to load the stored image")
                    return JsonResponse({'status': 'error', 'message': 'Failed to load the stored image'})

                # Convert the image to RGB
                stored_face_image = cv2.cvtColor(stored_face_image, cv2.COLOR_BGR2RGB)

                # Log the dimensions of the stored image
                logger.info(f"Stored image dimensions: {stored_face_image.shape}")

                # Get face encodings
                stored_face_encodings = face_recognition.face_encodings(stored_face_image)

                if stored_face_encodings:
                    stored_face_encoding = stored_face_encodings[0]
                    match = face_recognition.compare_faces([stored_face_encoding], uploaded_face_encoding)

                    if match[0]:
                        return JsonResponse({'status': 'success', 'message': 'Welcome'})
                    else:
                        return JsonResponse({'status': 'error', 'message': 'Face does not match'})
                else:
                    logger.error("No face detected in the stored image")
                    return JsonResponse({'status': 'error', 'message': 'No face detected in the stored image'})
            else:
                logger.error("No face detected in the uploaded image")
                return JsonResponse({'status': 'error', 'message': 'No face detected in the uploaded image'})
        except Exception as e:
            logger.error(f"Error during face recognition: {e}")
            return JsonResponse({'status': 'error', 'message': str(e)})

    return render(request, 'login.html')

def welcome(request):
    return render(request, 'welcome.html')  