from neo4j import GraphDatabase


def query_neo4j_list(
    IP_SERVER_NEO4J: str, USER_NEO4J: str, PASSWORD_NEO4J: str, query: str
):
    driver = GraphDatabase.driver(IP_SERVER_NEO4J, auth=(USER_NEO4J, PASSWORD_NEO4J))
    with driver.session() as session:
        result = session.run(query)
        res = result.data()
        driver.close()
        return list(res)


def query_neo4j_str(
    IP_SERVER_NEO4J: str, USER_NEO4J: str, PASSWORD_NEO4J: str, query: str
):
    driver = GraphDatabase.driver(IP_SERVER_NEO4J, auth=(USER_NEO4J, PASSWORD_NEO4J))
    with driver.session() as session:
        session.run(query)
        driver.close()
