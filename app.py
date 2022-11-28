from flask import Flask, request
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
    args = request.args
    filter_query = f"""FILTER(?attraction_subject IN ({createAttractionSubjectsList(categoriesSet)}))""" if args.get('category') else ""
    query = f"""
        SELECT DISTINCT ?attraction 
        WHERE {{
            ?attraction dct:subject ?attraction_subject ;
                        dbo:location dbr:{city} .            
            
            {filter_query}
        }}
    """

    sparql.setQuery(query)
    sparql.setReturnFormat(JSON)

    result = sparql.query().convert()
    response = fetchResponseFromSPARQLWrapper(result)

    return response


@app.route('/regions/<region>/attractions', methods=['GET'])
def regionAttractions(region):
    args = request.args
    filter_query = f"""FILTER(?attraction_subject IN ({createAttractionSubjectsList(categoriesSet)}))""" if args.get(
        'category') else ""
    query = f"""
        SELECT DISTINCT ?attraction ?attraction_thumbnail ?attraction_label ?attraction_description GROUP_CONCAT(DISTINCT ?attraction_more_details; separator=",") as ?attraction_more_details_grouped
        WHERE {{
            ?attraction dct:subject ?attraction_subject ;
                        dbo:location dbr:{region} ;
                        dbo:thumbnail ?attraction_thumbnail ;
                        rdfs:label ?attraction_label ;
                        dbo:abstract ?attraction_description ;
                        dbo:wikiPageExternalLink ?attraction_more_details .
                        
            FILTER (LANGMATCHES(LANG(?attraction_label), "uk"))
            FILTER (LANGMATCHES(LANG(?attraction_description), "uk"))   

            {filter_query}
        }}
        GROUP BY ?attraction ?attraction_description ?attraction_label ?attraction_thumbnail
    """

    sparql.setQuery(query)
    sparql.setReturnFormat(JSON)

    result = sparql.query().convert()
    response = fetchResponseFromSPARQLWrapper(result)

    print(response)

    return list(map(lambda r: { 'details': r['attraction_more_details_grouped']['value'].split(','), 'attraction': r['attraction']['value'], 'description': r['attraction_description']['value'], 'label': r['attraction_label']['value'], 'thumbnail': r['attraction_thumbnail']['value'] }, response))

@app.route('/categories', methods=['GET'])
def categories():
    return list(categoriesSet)

if __name__ == '__main__':
    app.run(debug=True)
