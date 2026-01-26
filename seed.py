from config import get_db

def setup_scenario():
    driver = get_db()

    money_query = """
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

    device_query = """
    MATCH(a:User {name: "Alpha"})
    MATCH(b:User {name: "Beta"})
    MATCH(c:User {name: "Gamma"})
    
    MERGE (iphone: Phone {id: "IPhone_14" , ip: "190.072.441.1000"})
    MERGE (redmi: Phone {id: "Redmi_Note17", ip: "110.450.089.3000"})
    
    MERGE (a)-[:USED_DEVICE]->(iphone)
    MERGE (b)-[:USED_DEVICE]->(iphone)
    MERGE (c)-[:USED_DEVICE]->(redmi)
    
    """
    with driver.session() as session:
        session.run(money_query)
        print("Data Seeded. The trap has been set.")
        session.run(device_query)
        print("Device Data Successfully Seeded.")

if __name__ == "__main__":
    setup_scenario()