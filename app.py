from flask import Flask, request, jsonify
from rdflib import Graph 
from SPARQLWrapper import SPARQLWrapper, JSON, N3
from pprint import pprint

app = Flask(__name__)

@app.route("/")
def index():
    sparql = SPARQLWrapper('https://dbpedia.org/sparql')
    sparql.setQuery('''
        SELECT ?object
        #WHERE { dbr:Personal_finance rdfs:label ?object .}
        WHERE { dbr:Personal_finance dbo:abstract ?object .}
    ''')

    sparql.setReturnFormat(JSON)
    qres = sparql.query().convert()

    #pprint(qres)
    for result in qres['results']['bindings']:
        #print(result['object'])
        
        lang, value = result['object']['xml:lang'], result['object']['value']
        # print(f'Lang): {lang}\tValue: {value}')
        if lang == 'en':
            return value

@app.route("/structure")
def structure(): 
    sparql = SPARQLWrapper("https://dbpedia.org/sparql")

    sparql.setQuery('''
    CONSTRUCT { dbc:Personal_finance skos:broader ?parent .
                dbc:Personal_finance skos:narrower ?child .}
    WHERE {
        { dbc:Personal_finance skos:broader ?parent . }
    UNION
        { ?child skos:broader dbc:Personal_finance . }
    }
    ''')

    sparql.setReturnFormat(N3)
    qres = sparql.query().convert()

    g = Graph()
    g.parse(data=qres, format='n3')
    structure = g.serialize(format='ttl').decode('u8')
    return (structure)

if __name__ == '__main__':
    app.run()