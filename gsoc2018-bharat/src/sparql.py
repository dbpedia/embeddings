from SPARQLWrapper import SPARQLWrapper, JSON
import asyncio
from urllib.error import HTTPError
from SPARQLWrapper.SPARQLExceptions import EndPointInternalError
import json

sparql = SPARQLWrapper("http://dbpedia.org/sparql")
final_pool = []

query = """
    PREFIX rdfs:<http://www.w3.org/2000/01/rdf-schema#>
    PREFIX rdf:<http://www.w3.org/1999/02/22-rdf-syntax-ns#>
    PREFIX dbo: <http://dbpedia.org/ontology/>
    SELECT DISTINCT ?s ?abstract ?url ?p
    WHERE {
        ?s a/rdfs:subClassOf* dbo:Organisation .
        ?s foaf:isPrimaryTopicOf ?url ;
            a ?p .
        ?p a owl:Class .
        ?s dbo:abstract ?abstract .
        filter(langMatches(lang(?abstract), "en"))
    }
LIMIT 10000 OFFSET """


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


futures = [fetch_data(query + str(i * 10000), i) for i in range(0, 50)]
loop = asyncio.get_event_loop()
loop.run_until_complete(asyncio.wait(futures))
count = 0
with open('data/dbpedia_dictionary.json', 'w+') as abstract_dictionary:
    with open('data/classes_dictionary.json', 'w+') as class_dictionary:
        for line in final_pool:
            print('Abstracts : {0}'.format(count), end='\r')
            a = {}
            c = {}
            entity = ''
            t = ''
            entity = line['s']['value']
            entity = entity.replace('http://dbpedia.org/resource/', '')
            entity = entity.lower()
            a[entity] = line['abstract']['value'].lower()
            t = line['p']['value']
            c[entity] = t.replace('http://dbpedia.org/ontology/', '')
            json.dump(a, abstract_dictionary)
            abstract_dictionary.write('\n')
            json.dump(c, class_dictionary)
            class_dictionary.write('\n')
            count += 1
