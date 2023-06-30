from SPARQLWrapper import SPARQLWrapper, JSON, GET


def property_between_individuals(
    IP_SERVER_NEO4J: str,
    USER_NEO4J: str,
    PASSWORD_NEO4J: str,
    sparql_service: str,
    API_KEY: str,
    uri_1: str,
    uri_2: str,
):

    sparql = SPARQLWrapper(sparql_service)
    if sparql_service == "http://sparql.bioontology.org/sparql/":
        sparql.addCustomParameter("apikey", API_KEY)

    query_sparql = f"""
                SELECT DISTINCT  ?property
                WHERE {{ 
                    <{uri_1}>  ?property <{uri_2}>.
                    }}"""

    sparql.setQuery(query_sparql)
    sparql.setReturnFormat(JSON)
    if sparql_service != "http://sparql.bioontology.org/sparql/":
        sparql.setMethod(GET)
    try:
        if len(sparql.query().convert()["results"]["bindings"]) > 0:
            for response in sparql.query().convert()["results"]["bindings"]:
                property_btw_i = response["property"]["value"]
        else:
            property_btw_i = None

    except:
        property_btw_i = None
    return property_btw_i
