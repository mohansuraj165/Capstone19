def ParseWaysData(ways):
    wayIDs = dict()
    for w in ways:
        if w['type'] == "way" and 'tags' in w:
            tags = w['tags']
            if 'name' in tags:
                wayIDs[tags.get('name')] = w.get('id')
                #########################
                #store final values in DB
                #########################
    return (wayIDs)


def Associate(nodes, ways):
    wayIDs = ParseWaysData(ways)
    for n in nodes:
        if n.street in wayIDs:
            print (n.street)

