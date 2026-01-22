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
    MATCH path = (receiver:Account {id: $to_id})-[:TRANSFERRED*1..4]->(sender:Account {id: $from_id})
    RETURN length(path) AS hops
    """

    with driver.session() as session:
        result = session.run(cypher_check,to_id = tx.to_acc,from_id = tx.from_acc)
        record = result.single()

        if record:
            hops = record["hops"]
            return {
                "status": "BLOCKED",
                "reason": f"Circular fraud detected! Money returns to sender in {hops} hops."
            }
        session.run("""
        MATCH (a:Account {id: $from_ac}), (b:Account {id: $to_ac})
        CREATE (a)-[:TRANSFERRED {amount: $amt}]->(b)
        """, from_ac = tx.from_acc, amt = tx.amount , to_ac = tx.to_acc)

        return{"status": "APPROVED","reason": "Transaction is Safe"}

