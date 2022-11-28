# A list of categories that represents attractions all over Ukraine
categoriesSet = {
 "dbc:Eastern_Orthodox_monasteries_in_Ukraine",
 "dbc:Religious_museums_in_Ukraine",
 "dbc:World_Heritage_Sites_in_Ukraine",
 "dbc:Historic_sites_in_Ukraine",
 "dbc:Protected_areas_of_Ukraine",
 "dbc:Allegorical_sculptures_in_Ukraine",
 "dbc:Outdoor_sculptures_in_Ukraine",
 "dbc:Colossal_statues_in_Ukraine",
 "dbc:Rebuilt_buildings_and_structures_in_Ukraine",
 "dbc:20th-century_Roman_Catholic_church_buildings_in_Ukraine"
}

def fetchResponseFromSPARQLWrapper(res):
 return res['results']['bindings']
