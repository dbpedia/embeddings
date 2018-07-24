from SPARQLWrapper import SPARQLWrapper, JSON
import asyncio
from urllib.error import HTTPError
from SPARQLWrapper.SPARQLExceptions import EndPointInternalError

sparql = SPARQLWrapper("http://dbpedia.org/sparql")
final_pool = []
query = """
    PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
    PREFIX dbo: <http://dbpedia.org/ontology/>
    SELECT DISTINCT ?s ?abstract WHERE {
        ?s a/rdfs:subClassOf* dbo:Organisation .
        ?s dbo:abstract ?abstract .
        filter(langMatches(lang(?abstract), "en"))
    }
    LIMIT 10000 OFFSET """

# queries = [query + str(i * 10000) for i in range(0, 5)]


async def fetch_data(q, i):
    """
    Async call to DBpedia, making sparql queries
    to get the abstracts of entities of type 'Organisation'

    Arguments
    ---------
    q : query to be made
    i : request id
    """
    global final_pool
    print(f'INFO : sending request # {i + 1}')
    sparql.setQuery(q)
    sparql.setReturnFormat(JSON)
    try:
        results = sparql.query().convert()
    except (HTTPError, EndPointInternalError) as _:
        fetch_data(q, i)

    data = results['results']['bindings']
    final_pool = final_pool + data
    print(f'INFO : completed request # {i + 1}')


futures = [fetch_data(query + str(i * 10000), i) for i in range(0, 2)]
loop = asyncio.get_event_loop()
loop.run_until_complete(asyncio.wait(futures))
print(len(final_pool))
