import sqlite3
from sqlite3 import Error

conn = None
db_file = "TempDB.db"
def CreateDBConnection():
    """ create a database connection to a SQLite database """
    global conn
    try:
        conn = sqlite3.connect(db_file)
        print('DB created')
        CreateWaysTable()
        CreateAssociatedNodesTable()
    except Error as e:
        print(e)

def OpenConnection():
    """ opens a database connection """
    global conn
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except Error as e:
        print(e)

def GetConnection():
    global conn
    return conn

def CloseConnection():
    global conn
    conn.close()

def CreateWaysTable():
    global conn
    qry="CREATE TABLE IF NOT EXISTS TBL_WAYS" \
        "(WayID TEXT NOT NULL," \
        "NodeIDs TEXT NOT NULL," \
        "Street VARCHAR NOT NULL);"
    try:
        conn.execute(qry)
        print('Ways created')
    except Error as e:
        print(e)

def CreateAssociatedNodesTable():
    global comm
    qry = "CREATE TABLE IF NOT EXISTS TBL_ASSOCIATED_NODES " \
          "(WayID TEXT NOT NULL," \
          "Node TEXT NOT NULL);"
    try:
        conn.execute(qry)
        print('Associated nodes created')
    except Error as e:
        print(e)

def SelectWayByStreet(street):
    global conn
    c = conn.cursor()
    qry="SELECT * FROM TBL_WAYS WHERE Street like '%s';"%street
    try:
        c.execute(qry)
        return c.fetchone()
    except Error as e:
        print(e)

def InsertIntoAssociatedNodes(wayId,node):
    global conn
    c = conn.cursor()
    qry = "INSERT INTO TBL_ASSOCIATED_NODES (WayID,Node)" \
          "VALUES ('%s','%s')"%(wayId,node)
    try:
        c.execute(qry)
    except Error as e:
        print(e)

def InsertIntoWays(wayID,nodeIDs,street):
    global conn
    c = conn.cursor()
    qry = "INSERT INTO TBL_WAYS (WayID,NodeIDs,Street)" \
          "VALUES('%s','%s','%s');"%(wayID,nodeIDs,street)
    try:
        conn.execute(qry)
    except Error as e:
        print(e)
