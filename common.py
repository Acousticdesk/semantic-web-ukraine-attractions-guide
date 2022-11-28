# A list of categories that represents attractions all over Ukraine
subjectSet = {
 "dbc:World_Heritage_Sites_in_Ukraine",
 "dbc:Allegorical_sculptures_in_Ukraine",
 "dbc:Outdoor_sculptures_in_Ukraine",
 "dbc:Colossal_statues_in_Ukraine",
 "dbc:National_parks_of_Ukraine",
 "dbc:Ukrainian_restaurants",
}

typeSet = {
 "dbo:ArchitecturalStructure",
 "dbo:Reservoir",
 "dbo:ProtectedArea",
 "dbo:Museum",
 "dbo:Airport",
 "dbo:HistoricBuilding",
 "dbo:Stadium",
}

def fetchResponseFromSPARQLWrapper(res):
 return res['results']['bindings']
