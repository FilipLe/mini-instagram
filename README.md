# Mini Insta

A simple Instagram clone built with Django. Users can create profiles, post photos with captions, follow others, like and comment on posts, and view personalized feeds.

## Features
- User authentication (register, login, logout)
- Profile creation and editing (username, display name, bio, profile picture)
- Create, update, and delete posts with multiple photos
- Follow/unfollow users
- Like/unlike posts
- Comment on posts
- View followers/following lists
- Personalized feed of posts from followed users
- Search for profiles and posts by keywords
- Responsive HTML templates for profiles, posts, and feeds

## Technologies Used
- Python 3.x
- Django 4.x (or compatible version)
- HTML5 & CSS3 for frontend
- SQLite (default database, can be swapped)

## Installation
1. Clone the repository:
   ```
   git clone https://github.com/FilipLe/mini-instagram.git
   cd mini-insta
   ```

2. Create and activate a virtual environment:
   ```
   pipenv shell
   ```

3. Install dependencies:
   ```
   pip install django
   ```
   *Note: Add other dependencies like Pillow for image handling if needed.*

4. Apply migrations:
   ```
   python manage.py makemigrations
   python manage.py migrate
   ```

5. Run the development server:
   ```
   python manage.py runserver
   ```
   Open `http://127.0.0.1:8000/` in your browser.

## Usage
- Register a new account via the "Register" link.
- Log in to create posts, follow users, and interact.
- View all profiles at the home page.
- Access your profile, feed, and search from the navigation footer.
- Admin panel: `/admin` (log in with superuser credentials).
