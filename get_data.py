import rdflib
import duckdb

g = rdflib.Graph()
g.parse("incite_with_data.ttl")
db = duckdb.connect("data.db")

# get all data sources for indoor temperature
query = """
PREFIX ref: <https://brickschema.org/schema/Brick/ref#>
SELECT ?sensor ?label ?table WHERE {
    <urn:incite_example/building> brick:hasPoint ?sensor .
    ?sensor a brick:Air_Temperature_Sensor ;
            ref:hasExternalReference ?ref .
    ?ref ref:hasTimeseriesId ?label ;
         ref:onTable ?table .
}"""
for row in g.query(query):
    sensor, label, table = row
    duck_query = f"SELECT Timestamp, {label} FROM {table}"
    res = db.sql(duck_query)
    print(f"Sensor {sensor} has {len(res)} values in table {table}")

print('-' * 30)

# get all meter power data for a given scenario
scenario = 'RBC_Cost_Cool'
query = f"""
PREFIX ref: <https://brickschema.org/schema/Brick/ref#>
SELECT ?meter ?point ?label WHERE {{
    ?meter a brick:Meter ;
        brick:hasPoint ?point .
    ?point brick:hasUnit unit:KiloW ;
        ref:hasExternalReference ?ref .
    ?ref ref:onTable "{scenario}" ;
        ref:hasTimeseriesId ?label .
}}"""
    
for row in g.query(query):
    meter, point, label = row
    print(meter, point, label)
    duck_query = f"SELECT Timestamp, {label} FROM {scenario}"
    res = db.sql(duck_query)
    print(f"Sensor {point} on meter {meter} has {len(res)} values in scenario {scenario}")
