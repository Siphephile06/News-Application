# 📰 News Application

This is a Django-based News Application that can be run locally using Python's `venv` or containerized with Docker.

---

## 🔧 Setup with Python Virtual Environment (venv)

1. **Create and activate a virtual environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate

2. # Install dependencies

pip install -r requirements.txt

3. Configure Environment Variables
Copy the example file and fill in your values:

Bash
cp .env.example .env


4. # Apply migrations and run the server.

python manage.py migrate
python manage.py runserver

🐳 Running with Docker
1. # Build the Docker image:

docker build -t news-app .

2. # Run the container:

docker run --env-file .env -d -p 8000:8000 news-app

3. # Access the application:

Visit http://localhost:8000 in your browser.








