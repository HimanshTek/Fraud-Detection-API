# Neo4j Fraud Detector API

A real-time fraud detection engine built with **FastAPI** and **Neo4j**. 
It uses Graph Algorithms to detect "Circular Money Laundering" patterns in financial transactions.

## 🚀 Tech Stack
* **Python 3.10+**
* **FastAPI** (High-performance API)
* **Neo4j** (Graph Database for relationship analysis)

## 🛠️ How to Run
1.  **Install Dependencies:** `pip install -r requirements.txt`
2.  **Setup Database:** * Install Neo4j Desktop and start a Local DBMS.
    * Rename `config_example.py` to `config.py` and update the password.
3.  **Seed Data:** `python seed.py`
4.  **Start Server:** `uvicorn main:app --reload`
5.  **Test API:** Go to `http://127.0.0.1:8000/docs`

## 🧠 Logic
The API prevents "Round Tripping" (A -> B -> C -> A) by checking for cycles in the graph before approving a transaction.

## SideNote
This is my first mini project trying to use FastAPI and Neo4j for an actual application.