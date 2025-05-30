## ⚡ Quick Start

### 1️⃣ Clone the Repository
```bash
git clone https://github.com/hikehikehike/DeviIT.git
cd DeviIT
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

### 4️⃣ Access the API
Once running, open:

http://127.0.0.1:8000/api/docs

This opens FastAPI Swagger documentation.

### 5️⃣ Stop the Containers
To stop the containers, use:

```bash
docker-compose down
```
