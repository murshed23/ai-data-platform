# 📊 Marketing AI Pipeline (Airflow + Vector + Graph)

An end-to-end data pipeline that simulates user conversations, generates embeddings, and stores data across multiple systems including MongoDB, FAISS, Neo4j, and SQLite, orchestrated using Apache Airflow.

---

## 🚀 Architecture
        +----------------------+
        |   Airflow DAG        |
        | marketing_ai_pipeline|
        +----------+-----------+
                   |
| | | | |
v v v v v

Generate Embeddings MongoDB FAISS Neo4j SQLite
Data (NLP) Storage Vector DB Graph DB Analytics


---

## 🧠 Pipeline Overview

The DAG `marketing_ai_pipeline` executes the following steps:

### 1️⃣ Generate Data (`generate_data`)
- Creates synthetic user conversations
- Fields:
  - `user_id`
  - `message`
  - `timestamp`
- Output:
/opt/airflow/dags/conversations.json


---

### 2️⃣ Generate Embeddings (`generate_embeddings`)
- Uses Sentence Transformers (`all-MiniLM-L6-v2`)
- Converts text → vector embeddings
- Output:
/opt/airflow/dags/embedded.json


---

### 3️⃣ Store in MongoDB (`store_mongodb`)
- Database: `marketing`
- Collection: `conversations`
- Stores:
- user data
- messages
- embeddings

---

### 4️⃣ Store in FAISS (`store_vector_db`)
- Builds vector index
- Enables similarity search
- Output:
/opt/airflow/dags/vector.index


---

### 5️⃣ Store in Neo4j (`store_graph_db`)
- Creates relationships:
(User)-[:INTERACTED]->(Campaign)


---

### 6️⃣ Store Analytics (`store_analytics_db`)
- Uses SQLite
- Stores engagement count per user

Table:
engagement(user_id, count)


File:
/opt/airflow/dags/analytics.db


---

## 🔁 DAG Flow
generate_data
↓
generate_embeddings
↓
store_mongodb
↓
store_vector_db
↓
store_graph_db
↓
store_analytics_db


---

## 🛠️ Tech Stack

- Apache Airflow
- MongoDB
- FAISS
- Neo4j
- SQLite
- Sentence Transformers
- Docker & Docker Compose

---

## ⚙️ Setup Instructions
```bash
1️⃣ Clone the repository
git clone <your-repo-url>
cd FDE_Assignment

2️⃣ Start services
docker compose up --build

3️⃣ Access Airflow
http://localhost:8080
Login:

username: admin
password: admin

4️⃣ Run the Pipeline
Enable DAG: marketing_ai_pipeline

Click Trigger DAG


🔍 Verification
MongoDB
docker exec -it <mongodb-container> mongosh
use marketing
db.conversations.find().limit(5)
Neo4j
http://localhost:7474
MATCH (n) RETURN n LIMIT 10;
FAISS
Check file:

airflow/dags/vector.index
SQLite
sqlite3 airflow/dags/analytics.db
SELECT * FROM engagement LIMIT 10;
Airflow
Ensure all tasks are green.

📂 Project Structure
FDE_Assignment/
│
├── airflow/
│   └── dags/
│       ├── pipeline.py
│       ├── conversations.json
│       ├── embedded.json
│       ├── vector.index
│       └── analytics.db
│
├── docker-compose.yml
└── README.md

📌 Example Output
MongoDB
{
  "user_id": "user_1",
  "message": "I want to buy shoes",
  "embedding": [...]
}

Neo4j
(User)-[:INTERACTED]->(Campaign)

SQLite
user_1 → 5
user_2 → 3

⚠️ Notes
Uses host.docker.internal for DB connections

First run downloads NLP model (may take time)

Ensure Docker Desktop is running

🚀 Improvements (Optional)
Add Redis caching layer

Add FastAPI for recommendations

Use cloud storage (S3/GCS)

Add Kafka for streaming

📜 License
For educational and assessment purposes

```
