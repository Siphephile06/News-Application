📰 News Application

A Django-based News Application that allows users to view, manage, and publish news articles. It can be run locally using Python's virtual environment or containerized with Docker.

📦 Features

- User authentication and session management
- Article creation, editing, and approval workflows
- Role-based contributor dashboards (e.g., editors, journalists)
- Email and social media notifications for subscribers
- Responsive UI with static asset management
- Environment variable support for secure configuratio

🚀 Getting Started

🔧 Local Setup with Python Virtual Environment

1. Create and Activate a Virtual Environment

python -m venv venv

source venv/bin/activate  # On Windows: venv\Scripts\activate


2. Install Dependencies
   
pip install -r requirements.txt


3. Configure Environment Variables
   
Copy the example file and fill in your values:

cp .env.example .env


Make sure to include all required variables. Refer to the README section Environment Variables below for details.

4. Apply Migrations and Start the Server

python manage.py migrate

python manage.py runserver


Visit http://localhost:8000 to access the application.

🐳 Running with Docker

1. Build the Docker Image

docker build -t news-app .


2. Run the Container

docker run --env-file .env -d -p 8000:8000 news-app


Visit http://localhost:8000 in your browser.

🔐 Environment Variables

Ensure your .env file includes all required variables.

Refer to .env.example for a complete list.

🧪 Running Tests

python manage.py test


📚 Documentation

Auto-generated documentation is available via Sphinx. To build it locally:

cd docs

make html  # On Windows: .\make.bat html


Open docs/_build/html/index.html in your browser.

👥 Contributor Guide

- Ensure .env is configured correctly
- Follow PEP8 and Django best practices
- Use feature branches and submit pull requests
- Update documentation and tests for new features

🛠️ Troubleshooting

- Static files not loading? Run python manage.py collectstatic
- Login/session issues? Check browser cookies and session middleware
- Docker not working? Ensure .env is correctly passed and ports are available

