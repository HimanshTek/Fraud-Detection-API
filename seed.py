from config import get_db

def setup_scenario():
    driver = get_db()

    query = """
    MERGE(a:User {name: "Alpha"})
    MERGE(b:User {name: "Beta"})
    MERGE(c:User {name: "Gamma"})
    
    MERGE(acc1:Account {id: "ACC_100"})
    MERGE(acc2:Account {id: "ACC_200"})
    MERGE(acc3:Account {id: "ACC_300"})
    
    MERGE (a)-[:OWNS]->(acc1)
    MERGE (b)-[:OWNS]->(acc2)
    MERGE (c)-[:OWNS]->(acc3)
    
    MERGE (acc1)-[:TRANSFERRED]->(acc2)
    MERGE (acc2)-[:TRANSFERRED]->(acc3)
    """
    with driver.session() as session:
        session.run(query)
        print("Data Seeded. The trap has been set.")

if __name__ == "__main__":
    setup_scenario()