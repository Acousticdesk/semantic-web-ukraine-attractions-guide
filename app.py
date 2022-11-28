from flask import Flask
from SPARQLWrapper import SPARQLWrapper, JSON
from flask_cors import CORS
from common import categoriesSet, fetchResponseFromSPARQLWrapper
from helpers import createAttractionSubjectsList

app = Flask(__name__)
CORS(app)

sparql = SPARQLWrapper('https://dbpedia.org/sparql')

@app.route('/regions', methods=['GET'])
def regions():
    query = """
        SELECT ?region 
        WHERE {
            ?region dct:subject dbc:Oblasts_of_Ukraine .
        }
    """

    sparql.setQuery(query)
    sparql.setReturnFormat(JSON)

    result = sparql.query().convert()
    response = fetchResponseFromSPARQLWrapper(result)

    return list(map(lambda r: r['region']['value'], response))

@app.route('/regions/<region>/cities', methods=['GET'])
def cities(region):
    query = f"""
        SELECT ?city 
        WHERE {{
            ?city dbo:subdivision dbr:{region} .
        }}
    """

    sparql.setQuery(query)
    sparql.setReturnFormat(JSON)

    result = sparql.query().convert()
    response = fetchResponseFromSPARQLWrapper(result)

    return list(map(lambda r: r['city']['value'], response))

@app.route('/cities/<city>/attractions', methods=['GET'])
def cityAttractions(city):
    query = f"""
        SELECT DISTINCT ?attraction 
        WHERE {{
            ?attraction dct:subject ?attraction_subject ;
                        dbo:location dbr:{city} .            
            
            FILTER(?attraction_subject IN ({createAttractionSubjectsList(categoriesSet)}))
        }}
    """

    sparql.setQuery(query)
    sparql.setReturnFormat(JSON)

    result = sparql.query().convert()
    response = fetchResponseFromSPARQLWrapper(result)

    return response

if __name__ == '__main__':
    app.run(debug=True)
