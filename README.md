# News Application

A Django-based platform for publishing, managing, and viewing news articles. Supports local development and Docker deployment, with role-based dashboards and social media integration.

# Table of Contents

- Project Overview
- Features
- Installation
  * Local Setup
  * Docker Setup
- Usage
- Environment Variables
- Testing
- Documentation
- Contributor Guide
- Troubleshooting

# Project Overview

This application provides a simple interface for managing news articles, including:

- Article creation and editing
- User authentication
- Role-based access (e.g., editors, contributors)
- Dockerized deployment
- Environment-based configuration


# Features

- 🔐 User authentication and session management
- 📝 Article creation, editing, and approval workflows
- 👥 Role-based dashboards for editors and journalists
- 📣 Email and social media notifications for subscribers
- 💻 Responsive UI with static asset management
- 🔧 Secure configuration via environment variable

# Installation

## Local Setup

1.) Create and activate a virtual environment

```python -m venv venv```

source venv/bin/activate  # On Windows: venv\Scripts\activate

2.) Install dependencies:

```pip install -r requirements.txt```

3.) Configure environment variables:

```cp .env.example .env```

- Fill in all required values. See Environment Variables.

4.) Apply migrations and start the server:

```python manage.py migrate```
```python manage.py runserver```

- Visit http://localhost:8000 to access the app.

# Docker Setup

1.) Build the Docker image:

```docker build -t news-app .```

2.) Run the container:

```docker run --env-file .env -d -p 8000:8000 news-app```

- Visit http://localhost:8000 in your browser.


# Usage

- Log in or register a user.
- Create and submit articles for approval.
- Editors can approve and publish articles.
- Subscribers recieve notifications for new posts.

# Testing

Run unit tests with:

```python manage.py test```

# Documentation

Auto-generated via Sphinx.

1.) Navigate to the docs folder.

```cd docs```

2.) Build the HTML docs.

```make html # on windows .\make.bat html

3.) Open docs/_build/html/index.html in your browser.


# Contributor Guide

- Ensure .env is configured correctly.
- Follow PEP8 and Django best practices.
- Use feature branches and submit pull requests.
- Update documentation and tests for new features.

# Troubleshooting

1.) Static files not loading?

Run:

```python manage.py collectstatic```

2.) Login/Session Issues?

- Check browser cookies and session middleware.

3.) Docker not working?

- Ensure .env is correctly passed and ports are available.










