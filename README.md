# ai-data-platform

📊 Marketing AI Pipeline (Airflow + Vector + Graph)
An end-to-end data pipeline that simulates user conversations, generates embeddings, and stores data across multiple systems including MongoDB, FAISS, Neo4j, and SQLite, orchestrated using Apache Airflow.

🚀 Architecture
            +----------------------+
            |   Airflow DAG        |
            | marketing_ai_pipeline|
            +----------+-----------+
                       |
   --------------------------------------------------
   |          |            |           |             |
   v          v            v           v             v

Generate   Embeddings   MongoDB     FAISS       Neo4j       SQLite
Data       (NLP)        Storage     Vector DB   Graph DB    Analytics
🧠 Pipeline Overview
The DAG marketing_ai_pipeline executes the following steps:

1️⃣ Generate Data (generate_data)
Creates synthetic user conversations

Fields:

user_id

message

timestamp

Saves to:

/opt/airflow/dags/conversations.json
2️⃣ Generate Embeddings (generate_embeddings)
Uses Sentence Transformers (all-MiniLM-L6-v2)

Converts message text → vector embeddings

Saves enriched data to:

/opt/airflow/dags/embedded.json
3️⃣ Store in MongoDB (store_mongodb)
Database: marketing

Collection: conversations

Stores:

user data

message

embeddings

4️⃣ Store in FAISS (store_vector_db)
Builds vector index using FAISS

Enables similarity search

Saves index file:

/opt/airflow/dags/vector.index
5️⃣ Store in Neo4j (store_graph_db)
Creates graph relationships:

(User)-[:INTERACTED]->(Campaign)
Example:

user_1 → campaign1
6️⃣ Store Analytics (store_analytics_db)
Uses SQLite

Stores engagement count per user

Table:

engagement(user_id, count)
File:

/opt/airflow/dags/analytics.db
🔁 DAG Execution Flow
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
🛠️ Tech Stack
Apache Airflow (Orchestration)

MongoDB (Document Store)

FAISS (Vector Database)

Neo4j (Graph Database)

SQLite (Analytics)

Sentence Transformers (NLP Embeddings)

Docker & Docker Compose

⚙️ Setup Instructions
1️⃣ Clone the repository
git clone <your-repo-url>
cd FDE_Assignment
2️⃣ Start all services
docker compose up --build
3️⃣ Access Airflow UI
http://localhost:8080
Login:

username: admin
password: admin
4️⃣ Run the Pipeline
Enable DAG: marketing_ai_pipeline

Click Trigger DAG

🔍 Verification Steps
✅ MongoDB
docker exec -it <mongodb-container> mongosh
use marketing
db.conversations.find().limit(5)
✅ Neo4j
Open:

http://localhost:7474
Run:

MATCH (n) RETURN n LIMIT 10;
✅ FAISS
Check if file exists:

airflow/dags/vector.index
✅ SQLite Analytics
sqlite3 airflow/dags/analytics.db
SELECT * FROM engagement LIMIT 10;
✅ Airflow
Ensure all tasks are green in Graph View.

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
📌 Example Outputs
MongoDB Document
{
  "user_id": "user_1",
  "message": "I want to buy shoes",
  "embedding": [...]
}
Neo4j Graph
(User)-[:INTERACTED]->(Campaign)
SQLite Analytics
user_1 → 5 interactions
user_2 → 3 interactions
⚠️ Notes
MongoDB & Neo4j connections use:

host.docker.internal
Ensure Docker Desktop is running

First run may take time due to model download

🚀 Possible Improvements
Add Redis caching layer (currently not used)

Add FastAPI for recommendation API

Replace SQLite with data warehouse (BigQuery/Snowflake)

Add real-time streaming (Kafka)

🧑‍💻 How to Use
Run Docker containers

Trigger Airflow DAG

Inspect:

MongoDB → raw + embedded data

Neo4j → graph relationships

FAISS → vector index

SQLite → analytics

📜 License
For educational and assessment purposes.

