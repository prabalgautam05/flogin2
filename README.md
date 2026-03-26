# flogin2 - Face Recognition Login System

A Django-based web application that implements face recognition technology for user authentication. Users can register with a face image and login using facial recognition instead of traditional passwords.

## Features

- **Face-based Registration**: Users register by capturing a face image alongside their username
- **Face Recognition Login**: Authenticate users by comparing facial features against stored face encodings
- **User Management**: Built-in user account management with Django's User model
- **Real-time Face Detection**: Uses OpenCV and dlib for face detection and encoding
- **Secure Authentication**: CSRF protection and error handling for security
- **Responsive Web Interface**: Clean UI with templates for login, register, and welcome pages

## Technology Stack

- **Backend**: Django 5.1.7
- **Face Recognition**: face_recognition, dlib, OpenCV
- **Database**: SQLite3
- **Frontend**: HTML/CSS (Bootstrap compatible)
- **Image Processing**: Pillow, NumPy

## Requirements

- Python 3.10 only
- Django 5.1.7
- face_recognition
- opencv-python
- dlib
- Pillow
- NumPy

All dependencies are listed in `requirements.txt`

## Installation

### 1. Clone the Repository
```bash
git clone <repository-url>
cd flogin2
```

### 2. Create Virtual Environment
```bash
python -m venv facelogin_env
```

### 3. Activate Virtual Environment
- **Windows (Command Prompt)**:
  ```bash
  facelogin_env\Scripts\activate
  ```
- **Windows (PowerShell)**:
  ```bash
  facelogin_env\Scripts\Activate.ps1
  ```
- **macOS/Linux**:
  ```bash
  source facelogin_env/bin/activate
  ```

### 4. Install Dependencies
```bash
pip install -r requirements.txt
```

### 5. Apply Database Migrations
```bash
python manage.py migrate
```

### 6. Create Superuser (Optional)
```bash
python manage.py createsuperuser
```

### 7. Run Development Server
```bash
python manage.py runserver
```

The application will be available at `http://127.0.0.1:8000/`

## Usage

### Registration
1. Navigate to `/accounts/register/` or click the Register link
2. Enter a username
3. Click "Capture Face" to capture your face image using your webcam
4. Click "Register" to create your account
5. Your face encoding is stored in the database for future authentication

### Login
1. Navigate to `/accounts/login/` or click the Login link
2. Enter your username
3. Click "Capture Face" to capture your face image using your webcam
4. Click "Login" to authenticate
5. If your facial features match the stored encoding, you'll be logged in successfully

### Welcome
Upon successful login, users are redirected to the welcome page displaying a personalized greeting.

## Project Structure

```
flogin2/
├── accounts/                 # User accounts app
│   ├── migrations/          # Database migrations
│   ├── templates/           # HTML templates
│   │   ├── login.html       # Login page
│   │   ├── register.html    # Registration page
│   │   └── welcome.html     # Welcome page
│   ├── models.py            # UserImage model
│   ├── views.py             # Authentication views
│   └── admin.py             # Admin configuration
├── flogin/                  # Main project settings
│   ├── settings.py          # Django settings
│   ├── urls.py              # URL routing
│   └── wsgi.py              # WSGI configuration
├── user_faces/              # Stored user face images directory
├── staticfiles/             # Static files (CSS, JS, admin assets)
├── db.sqlite3               # SQLite database
├── manage.py                # Django management script
└── requirements.txt         # Python dependencies
```

## Database Models

### UserImage
Stores the face image for each user:
- `user`: Foreign key to Django User model
- `face_image`: ImageField storing the captured face image

## API Endpoints

### Authentication Endpoints
- `POST /accounts/register/` - Register a new user with face image
- `POST /accounts/login/` - Authenticate user with face recognition
- `GET /accounts/welcome/` - Welcome page (after successful login)

## How Face Recognition Works

1. **Registration**:
   - User uploads face image during registration
   - `face_recognition.face_encodings()` generates a 128-dimensional face encoding
   - Encoding is stored in the database along with the original image

2. **Login**:
   - User provides uploaded face image and username
   - System generates face encoding from uploaded image
   - Compares uploaded encoding with stored encoding using `face_recognition.compare_faces()`
   - Returns success if faces match (Euclidean distance below threshold)

## Error Handling

The application includes comprehensive error handling for:
- User does not exist
- Face not detected in image
- Face mismatch during login
- Duplicate username registration
- Image loading failures

All errors are logged using Python's logging module for debugging purposes.

## Configuration

### Django Settings
Edit `flogin/settings.py` to:
- Configure database settings
- Add allowed hosts
- Configure static files directory
- Set secret key for production

### CSRF Exemption
Authentication endpoints are exempt from CSRF protection to allow face image uploads without a CSRF token. This is handled by the `@csrf_exempt` decorator.

## Security Considerations

- **Production**: Set `DEBUG = False` in settings.py for production deployment
- **Secret Key**: Change the Django secret key in production
- **HTTPS**: Use HTTPS in production to encrypt face images in transit
- **Database**: Use PostgreSQL or MySQL in production instead of SQLite
- **Media Files**: Configure appropriate permissions for the `user_faces/` directory

## Troubleshooting

### No Face Detected
- Ensure adequate lighting where you're capturing the image
- Position your face clearly in front of the camera
- Ensure your entire face is visible

### Face Does Not Match
- Ensure you're using the same device/angle as during registration
- Remove obstructions (sunglasses, hats, etc.)
- Ensure consistent lighting conditions

### dlib Installation Issues (Windows)
If you encounter issues installing dlib:
```bash
pip install dlib --only-binary :all:
```

## Future Enhancements

- Multi-factor authentication (face + PIN)
- Liveness detection to prevent spoofing attacks
- Multiple face enrollments per user
- Face recognition accuracy metrics
- Session management and logout functionality
- Admin dashboard for user management

## Contributing

Feel free to submit issues and enhancement requests!

## License

This project is open source and available under the MIT License.

## Support

For issues or questions, please open an issue in the repository.

