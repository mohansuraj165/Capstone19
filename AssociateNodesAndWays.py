import DB_eOSMGenerator as DB

def Associate(nodes):
    conn = DB.GetConnection()
    c=conn.cursor()
    for n in nodes:
        data = DB.SelectWayByStreet(n.street)
        DB.InsertIntoAssociatedNodes(data[0],n)

    qry="SELECT * FROM TBL_ASSOCIATED_NODES;"
    c.execute(qry)
    data=c.fetchall()
    for d in data:
        print(d[0],d[1])
