from flask import Flask
from SPARQLWrapper import SPARQLWrapper, JSON

app = Flask(__name__)

sparql = SPARQLWrapper('https://dbpedia.org/sparql')

# A list of categories that represents attractions all over Ukraine

# dbc:Eastern_Orthodox_monasteries_in_Ukraine
# dbc:Religious_museums_in_Ukraine
# dbc:World_Heritage_Sites_in_Ukraine
# dbc:Historic_sites_in_Ukraine
# dbc:Protected_areas_of_Ukraine
# dbc:Allegorical_sculptures_in_Ukraine
# dbc:Outdoor_sculptures_in_Ukraine
# dbc:Colossal_statues_in_Ukraine
# dbc:Rebuilt_buildings_and_structures_in_Ukraine
# dbc:20th-century_Roman_Catholic_church_buildings_in_Ukraine

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

    return result

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

    return result

# akicha todo: hardcoded categories to a constructor
@app.route('/cities/<city>/attractions', methods=['GET'])
def cityAttractions(city):
    query = f"""
        SELECT DISTINCT ?attraction 
        WHERE {{
            ?attraction dct:subject ?attraction_subject ;
                        dbo:location dbr:{city} .            
            
            FILTER(?attraction_subject IN (dbc:Eastern_Orthodox_monasteries_in_Ukraine, dbc:Religious_museums_in_Ukraine, dbc:World_Heritage_Sites_in_Ukraine))
        }}
    """

    sparql.setQuery(query)
    sparql.setReturnFormat(JSON)

    result = sparql.query().convert()

    return result

if __name__ == '__main__':
    app.run(debug=True)
