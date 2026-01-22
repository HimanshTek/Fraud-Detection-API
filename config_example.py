#config_example.py
#Add your database password and rename the file to config.py
from neo4j import GraphDatabase

URI = "neo4j://localhost:7687"
AUTH = ("neo4j","ADD_YOUR_PASSWORD_HERE")

driver = GraphDatabase.driver(URI,auth=AUTH)

def get_db():
    return driver
