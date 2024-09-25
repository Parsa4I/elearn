# E-Learn
Online learning and teaching platform with Django

## Features
- ### Enroll courses on different subjects
- ### Become an instructor and create your own courses
- ### Create modules for course in forms of text, image, video or file
- ### Chat room for courses
- ### Rate and comment
- ### Redis Cache, PostgreSQL database + Gunicorn and NGINX for production environment

## Usage
Run
```
$ docker compose up
```
and open `http://127.0.0.1:8000` on your browser :)

Or for production version:
```
$ docker compose -f docker-compose.prod.yml up
```
and open `http://127.0.0.1`.
