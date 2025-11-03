# LibraryProject

## Project Overview

**LibraryProject** is a Django application designed to manage a collection of books. This project serves as a foundational step in exploring Django's capabilities, including model creation, database interactions, and use of the Django admin interface.

## Objectives

1. **Set Up a Django Development Environment**: 
   - Install Django and create a basic project structure.
   - Understand the functionality of various components in a Django project.

2. **Implementing and Interacting with Django Models**:
   - Create a Django app named `bookshelf` within the project.
   - Define a `Book` model with attributes such as title, author, and publication year.
   - Perform basic CRUD (Create, Read, Update, Delete) operations using the Django shell.

3. **Utilizing the Django Admin Interface**:
   - Integrate the `Book` model with the Django admin interface.
   - Customize the admin display for better management of book data, including search and filtering capabilities.

## Getting Started

### Installation

1. Ensure Python is installed on your system.
2. Install Django using pip:
   pip install django

### Create a new Django Project
django-admin startproject LibraryProject

### Navigate to your Project Directory
cd LibraryProject

### Create an App 
python manage.py startapp bookshelf

### Prepare your model for database integration
python manage.py makemigrations bookshelf

### Apply migration
python manage.py migrate

### Run app
python manage.py runserver