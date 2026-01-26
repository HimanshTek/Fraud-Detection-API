from fastapi import FastAPI,HTTPException
from pydantic import BaseModel
from config import get_db

app = FastAPI()

class Transaction(BaseModel):
    from_acc: str
    to_acc: str
    amount: float

@app.post("/check_transaction")
def check_transaction(tx: Transaction):
    driver = get_db()

    cypher_check = """
    MATCH (r: Account {id: $to_id})
    MATCH (s: Account {id: $from_id})
    OPTIONAL MATCH path = (r)-[:TRANSFERRED*1..4]->(s)
    OPTIONAL MATCH device_link = (r)<-[:OWNS]-(x:User)-[:USED_DEVICE]->(d: Phone)<-[:USED_DEVICE]-(y:User)-[:OWNS]->(s)
    RETURN length(path) AS hops , d.id AS shared_device 
    """

    with driver.session() as session:
        result = session.run(cypher_check,to_id = tx.to_acc,from_id = tx.from_acc)
        record = result.single()

        if record and record["hops"]:
            hops = record["hops"]
            return {
                "status": "BLOCKED",
                "reason": f"Circular fraud detected! Money returns to sender in {hops} hops."
            }

        if record and record["shared_device"]:
            device = record["shared_device"]
            return {
                "status": "BLOCKED",
                "reason": f"Identity Fraud! Sender and Receiver use the same device: {device}."
            }

        session.run("""
        MATCH (a:Account {id: $from_ac}), (b:Account {id: $to_ac})
        CREATE (a)-[:TRANSFERRED {amount: $amt}]->(b)
        """, from_ac = tx.from_acc, amt = tx.amount , to_ac = tx.to_acc)

        return{"status": "APPROVED","reason": "Transaction is Safe"}

