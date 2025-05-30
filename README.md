## ⚡ Quick Start

### 1️⃣ Clone the Repository
```bash
git clone https://github.com/hikehikehike/viso
cd viso
```
In the .env file, replace the placeholder values with your actual API keys:

```bash
OPENAI_API_KEY=sk-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
WEATHER_API_KEY=abcdef1234567890abcdef1234567890
```

### 2️⃣ Ensure Docker is Installed
Check if Docker is installed:
```bash
docker --version
```
If not, download it from the [official website](https://www.docker.com/).

### 3️⃣ Build and Start the Containers

```bash
docker-compose up --build
```

Apply database migrations
```bash
docker-compose exec web python manage.py migrate
```
Create a user
```bash
docker-compose exec web python manage.py shell
```
Then in the Django shell, run:
```bash
from django.contrib.auth.models import User
User.objects.create_user(username="user1", password="user1pass")
exit()
```
Run the chat bot client in the terminal
```bash
docker-compose exec web python console_client.py
```


### 4️⃣ Access the API
Once running, open:

http://127.0.0.1:8000/api/docs

This Swagger documentation.

### 5️⃣ Stop the Containers
To stop the containers, use:

```bash
docker-compose down
```
