# 📚 Full-Stack Event-Driven Library System

This is a high-performance, microservices-based application for managing a library catalog. It demonstrates a modern **Event-Driven Architecture (EDA)** with asynchronous communication, full-text search, and automated containerization.

## 🏗 System Architecture

The project is split into two specialized backend services and a modern frontend:

1.  **Core Service:** Manages the source of truth (Books & Authors) in **MongoDB**. It acts as a **Kafka Producer**, emitting events whenever data changes.
2.  **Search Service:** Acts as a **Kafka Consumer**. It listens for events and synchronizes them into **Elasticsearch** for lightning-fast querying.
3.  **Frontend:** A **React** application that provides a unified interface for data entry and searching.

---

## 🛠 Tech Stack

- **Frontend:** React (Vite), Axios.
- **Backend:** Python 3.12, FastAPI, Motor (Async MongoDB), AIOKafka, Elasticsearch-py.
- **Databases:** MongoDB 7.0 (OLTP), Elasticsearch 8.12 (Search).
- **Messaging:** Apache Kafka (KRaft mode).
- **DevOps:** Docker, Docker Compose (Multi-stage builds), Environment Variables validation (Pydantic Settings).

---

## 🚦 Port Mapping & Navigation

Once the system is running, you can access the following services:

| Service             | URL                                                      | Purpose                                      |
| :------------------ | :------------------------------------------------------- | :------------------------------------------- |
| **Frontend UI**     | [http://localhost:5173](http://localhost:5173)           | Main user interface                          |
| **Core API Docs**   | [http://localhost:8000/docs](http://localhost:8000/docs) | Interactive Swagger UI for Write operations  |
| **Search API Docs** | [http://localhost:8001/docs](http://localhost:8001/docs) | Interactive Swagger UI for Search operations |
| **Kafka UI**        | [http://localhost:8080](http://localhost:8080)           | Visualizing topics, messages, and consumers  |
| **Elasticsearch**   | [http://localhost:9200](http://localhost:9200)           | Search engine health check                   |
| **MongoDB**         | `mongodb://localhost:27017`                              | Direct database access (via Compass)         |

---

## 🚀 Getting Started

### Prerequisites

- Docker and Docker Compose installed.
- Node.js (optional, only for local frontend development).

### Installation & Run

1.  **Clone the repository:**

    ```bash
    git clone <your-repo-url>
    cd <project-folder>
    ```

2.  **Launch the entire stack:**

    ```bash
    docker-compose up -d --build
    ```

3.  **Wait for initialization:**
    Kafka and Elasticsearch may take 15-20 seconds to fully boot up inside containers.

---

## 🔄 Data Flow Example

1.  User creates an **Author** via the UI.
2.  User creates a **Book**, linking it to the Author (Many-to-Many).
3.  `core-service` saves data to **MongoDB** and pushes a `book_created` event to **Kafka**.
4.  `search-service` consumes the event and indexes the book into **Elasticsearch**.
5.  The book becomes instantly searchable via the **Search Bar** in the UI.

---

## 🧪 Testing

Both backend services have unit and integration tests with coverage reporting.

### Prerequisites

```bash
# Create a virtualenv and install dependencies (includes test deps)
python3 -m venv .venv
source .venv/bin/activate
pip install -r core_service/requirements.txt -r search_service/requirements.txt
```

### Unit Tests (no Docker required)

```bash
# Core Service — models, routes, Kafka producer
cd core_service && pytest tests/unit -v
cd ..

# Search Service — search endpoints, reindex, Kafka consumer
cd search_service && pytest tests/unit -v
cd ..
```

### Integration Tests (requires running Docker stack)

```bash
docker compose up -d --build
# Wait ~30s for all services to become healthy

cd core_service && pytest tests/integration -v -m integration
cd ..

cd search_service && pytest tests/integration -v -m integration
cd ..
```

### Coverage Report

Coverage is collected automatically when running tests. After a test run, open `htmlcov/index.html` inside the respective service directory for a detailed HTML report.

---

## ⚙️ Configuration

The system is fully configurable via Environment Variables. See the `environment` section in `docker-compose.yml` to change database URLs or Kafka brokers without touching the source code.
