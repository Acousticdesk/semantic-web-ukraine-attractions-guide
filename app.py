from flask import Flask, request
from SPARQLWrapper import SPARQLWrapper, JSON
from flask_cors import CORS
from common import subjectSet, typeSet, fetchResponseFromSPARQLWrapper
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


@app.route('/regions/<region>/attractions', methods=['GET'])
def regionAttractions(region):
    args = request.args

    # categories_filter_query = f"""FILTER(?attraction_subject IN ({createAttractionSubjectsList(subjectSet)}))""" if args.get('category') else ""

    city_filter_query = f"""FILTER (?attraction_location IN (dbr:{args.get('city')}))""" if args.get('city') else f"""FILTER (?attraction_location IN (?city, dbr:{region}))"""

    query = f"""
        SELECT DISTINCT ?attraction ?attraction_thumbnail ?attraction_label ?attraction_description GROUP_CONCAT(DISTINCT ?attraction_more_details; separator=",") as ?attraction_more_details_grouped
        WHERE {{
            ?city dbo:subdivision dbr:{region} .
        
            ?attraction dct:subject ?attraction_subject ;
                        rdf:type ?attraction_type ;
                        dbo:location ?attraction_location ;
                        dbo:thumbnail ?attraction_thumbnail ;
                        rdfs:label ?attraction_label ;
                        dbo:abstract ?attraction_description ;
                        dbo:wikiPageExternalLink ?attraction_more_details .
                    
            {city_filter_query}
            FILTER(?attraction_subject IN ({createAttractionSubjectsList(subjectSet)}) || ?attraction_type IN ({createAttractionSubjectsList(typeSet)}))
            FILTER (LANGMATCHES(LANG(?attraction_label), "uk"))
            FILTER (LANGMATCHES(LANG(?attraction_description), "uk"))
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
    return list(subjectSet)

if __name__ == '__main__':
    app.run(debug=True)
