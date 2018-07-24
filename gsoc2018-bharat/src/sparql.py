from SPARQLWrapper import SPARQLWrapper, JSON
import asyncio


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
    print(f'Sending request # {i + 1}')
    sparql.setQuery(q)
    sparql.setReturnFormat(JSON)
    results = sparql.query().convert()
    data = results['results']['bindings']
    final_pool = final_pool + data


futures = [fetch_data(query + str(i * 10000), i) for i in range(0, 20)]
loop = asyncio.get_event_loop()
loop.run_until_complete(asyncio.wait(futures))
print(len(final_pool))
