from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime
import json
import random
from datetime import datetime as dt
from pymongo import MongoClient
from sentence_transformers import SentenceTransformer
import faiss
import numpy as np
from neo4j import GraphDatabase
import sqlite3

DATA_FILE = "/opt/airflow/dags/conversations.json"
EMBED_FILE = "/opt/airflow/dags/embedded.json"


# 1️⃣ Generate conversation data
def generate_data():
    users = [f"user_{i}" for i in range(50)]
    messages = [
        "I want to buy shoes",
        "Looking for discounts",
        "Need travel packages",
        "Interested in electronics"
    ]

    data = []

    for i in range(200):
        data.append({
            "user_id": random.choice(users),
            "message": random.choice(messages),
            "timestamp": str(dt.now())
        })

    with open(DATA_FILE, "w") as f:
        json.dump(data, f)

    print("Data generated")


# 2️⃣ Generate embeddings
def generate_embeddings():
    model = SentenceTransformer('all-MiniLM-L6-v2')

    data = json.load(open(DATA_FILE))

    for row in data:
        emb = model.encode(row["message"])
        row["embedding"] = emb.tolist()

    json.dump(data, open(EMBED_FILE, "w"))

    print("Embeddings created")


# 3️⃣ Store in MongoDB
def store_mongodb():

    client = MongoClient("mongodb://host.docker.internal:27017")
    db = client["marketing"]

    data = json.load(open(EMBED_FILE))

    db.conversations.insert_many(data)

    print("Stored in MongoDB")


# 4️⃣ Store in FAISS vector DB
def store_vector():

    data = json.load(open(EMBED_FILE))

    vectors = np.array([d["embedding"] for d in data]).astype("float32")

    index = faiss.IndexFlatL2(len(vectors[0]))
    index.add(vectors)

    faiss.write_index(index, "/opt/airflow/dags/vector.index")

    print("Stored in FAISS")


# 5️⃣ Store graph in Neo4j
def store_graph():

    driver = GraphDatabase.driver(
        "bolt://host.docker.internal:7687",
        auth=("neo4j", "password")
    )

    data = json.load(open(EMBED_FILE))

    with driver.session() as session:
        for d in data:
            session.run(
                """
                MERGE (u:User {id:$user})
                MERGE (c:Campaign {name:"campaign1"})
                MERGE (u)-[:INTERACTED]->(c)
                """,
                user=d["user_id"]
            )

    print("Stored in Neo4j")


# 6️⃣ Store analytics
def store_analytics():

    conn = sqlite3.connect("/opt/airflow/dags/analytics.db")

    conn.execute("""
    CREATE TABLE IF NOT EXISTS engagement(
        user_id TEXT,
        count INTEGER
    )
    """)

    data = json.load(open(EMBED_FILE))

    counts = {}

    for d in data:
        counts[d["user_id"]] = counts.get(d["user_id"], 0) + 1

    for k, v in counts.items():
        conn.execute(
            "INSERT INTO engagement VALUES (?,?)",
            (k, v)
        )

    conn.commit()

    print("Analytics stored")


# DAG definition
with DAG(
    dag_id="marketing_ai_pipeline",
    start_date=datetime(2024, 1, 1),
    schedule_interval=None,
    catchup=False
) as dag:

    task1 = PythonOperator(
        task_id="generate_data",
        python_callable=generate_data
    )

    task2 = PythonOperator(
        task_id="generate_embeddings",
        python_callable=generate_embeddings
    )

    task3 = PythonOperator(
        task_id="store_mongodb",
        python_callable=store_mongodb
    )

    task4 = PythonOperator(
        task_id="store_vector_db",
        python_callable=store_vector
    )

    task5 = PythonOperator(
        task_id="store_graph_db",
        python_callable=store_graph
    )

    task6 = PythonOperator(
        task_id="store_analytics_db",
        python_callable=store_analytics
    )

    task1 >> task2 >> task3 >> task4 >> task5 >> task6