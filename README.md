# 🇮🇳 Indian Cultural Atlas

## Overview

Indian Cultural Atlas is a Django-based web application designed to explore, preserve, and share the rich cultural heritage of India. The platform allows users to discover cultural information about Indian states and districts, including famous food, dances, folk arts, temples, monuments, festivals, traditional attire, and unique cultural characteristics.

Users can also contribute new cultural information, which is reviewed and approved by administrators before being published.

---

## Features

### Cultural Exploration

* Browse Indian States and Districts
* View cultural information and heritage details
* Explore:

  * Famous Foods
  * Traditional Dances
  * Folk Arts
  * Temples
  * Monuments
  * Festivals
  * Traditional Dresses
  * Cultural Uniqueness

### Search Functionality

* Search by:

  * State Name
  * District Name
  * Food
  * Temple
  * Festival
  * Monument
  * Folk Art

### User Authentication

* User Registration
* Login & Logout
* Password Management
* User Profile Management

### Cultural Contributions

* Submit State Cultural Information
* Submit District Cultural Information
* Separate submission forms for states and districts
* Admin approval workflow

### Admin Features

* Review submitted cultural information
* Approve or reject user submissions
* Manage states and districts through Django Admin

### Maps Integration

* Google Maps links for states and districts

---

## Technology Stack

### Backend

* Python
* Django

### Frontend

* HTML5
* CSS3
* Bootstrap 5

### Database

* SQLite

### Authentication

* Django Authentication System

---

## Project Structure

```text
Indian-Cultural-Atlas/
│
├── culture/
│   ├── models.py
│   ├── views.py
│   ├── forms.py
│   ├── admin.py
│   └── urls.py
│   ├── Templates/
│  
│  
├── templates/
├── static/
├── media/
├── db.sqlite3
├── manage.py
└── README.md
```

## Installation

### Clone the Repository

```bash
git clone <https://github.com/k-sruthi3/indian-cultural-atlas.git>
cd Indian-Cultural-Atlas
```

### Create Virtual Environment

```bash
python -m venv venv
```

### Activate Virtual Environment

Windows:

```bash
venv\Scripts\activate
```

Linux/Mac:

```bash
source venv/bin/activate
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

### Apply Migrations

```bash
python manage.py migrate
```

### Run Server

```bash
python manage.py runserver
```

Open:

```text
http://127.0.0.1:8000/
```

---

## Screenshots

Add screenshots of:
![About page](About_page.png)
![Admin_approval](Admin_approval.png)

![About page](About_page.png)

![About page](About_page.png)

![About page](About_page.png)

![About page](About_page.png)

* Home Page
* State Details Page
* District Details Page
* Search Feature
* User Profile
* State Submission Form
* District Submission Form
* Admin Approval Panel

---

## Future Enhancements

* AI-generated culture summaries
* Interactive cultural maps
* Contribution leaderboard
* User contribution history
* Cultural recommendation system
* Image gallery for states and districts
* API integration for cultural datasets

---

## Learning Outcomes

This project demonstrates:

* Django Models
* Django Forms
* Authentication & Authorization
* CRUD Operations
* Database Design
* Search Functionality
* Admin Customization
* Template Rendering
* Bootstrap UI Development

---

## Author

Developed as a cultural heritage exploration and preservation platform using Django.

Made with ❤️ for preserving India's cultural diversity.
