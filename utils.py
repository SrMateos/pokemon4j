from neo4j import GraphDatabase

def exec_query(query: str, params: dict):
    
    uri = "neo4j://localhost:7687"
    username = "neo4j"
    password = "password"
    database = "neo4j"
    
    with GraphDatabase.driver(uri, auth=(username, password)) as driver:
        records, summary, keys = driver.execute_query(query, params, database=database)
        return records, summary, keys