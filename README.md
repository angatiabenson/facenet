# FaceNet Project

## Overview

FaceNet is a sophisticated Django-based web application designed to leverage deep learning techniques for face recognition and metadata comparison tasks. It provides a RESTful API for uploading images, generating face metadata, and comparing this metadata between different images to determine similarity. This project aims to offer developers and users a robust platform for integrating face recognition capabilities into their applications.

## Features

- **Image Upload**: Securely upload images through a REST API.
- **Face Metadata Generation**: Extract face metadata from uploaded images.
- **Metadata Comparison**: Compare face metadata to find matches or similarities.
- **RESTful API**: Easy-to-use API endpoints for image processing and comparison.
- **Temporary Image Storage**: Temporarily store images for processing and automatically delete them afterward.

## Getting Started

### Prerequisites

- Python 3.8 or newer
- Django 3.2 or newer
- Django Rest Framework
- NumPy
- Other dependencies listed in `requirements.txt`

### Installation

1. **Clone the repository**

   ```
   git clone https://github.com/angatiabenson/facenet
   cd facenet
   ```
   
2. **Install dependencies**

   ```
   pip install -r requirements.txt
   ```

3. **Apply migrations**

   ```
   python manage.py makemigrations
   python manage.py migrate
   ```

4. **Run the server**

   ```
   python manage.py runserver
   ```

### Usage

The project provides two main API endpoints:

1. **Generate Face Metadata**

   - **Endpoint**: `/api/generate/face-metadata`
   - **Method**: POST
   - **Description**: Upload an image to generate and retrieve its face metadata.

2. **Compare Face Metadata**

   - **Endpoint**: `/api/compare/face-metadata`
   - **Method**: POST
   - **Description**: Submit two sets of face metadata to compare them and determine if they match.
