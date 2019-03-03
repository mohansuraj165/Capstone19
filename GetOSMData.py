import overpass
api = overpass.API()
#response = api.get('node["id"="62289870"]')
#MapQuery = overpass.MapQuery(50.7462,7.154,50.7463,7.157)
response = api.get('way(42.819,-73.881,42.820,-73.880);<;>;')
##WayQuery = overpass.WayQuery('[name="Highway 51"]')
#response = api.get(WayQuery)
print("done")
