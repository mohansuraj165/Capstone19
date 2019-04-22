import sqlite3
from sqlite3 import Error
import Logger as Log
import pickle

sqlite3.register_converter("pickle", pickle.loads)
sqlite3.register_adapter(list, pickle.dumps)
sqlite3.register_adapter(set, pickle.dumps)

conn = None
db_file = "OSM-OAImporterDB.db"

""" 
create a database connection to a SQLite database 
"""
def CreateDBConnection():

    global conn
    try:
        conn = sqlite3.connect(db_file)
        print('DB created')
        CreateWaysTable()
        CreateAssociatedNodesTable()
    except Error as e:
        print(e)
        Log.logging.error("In DBScript.py, CreateDBConnection()", exc_info=True)

""" 
opens a database connection 
"""
def OpenConnection():

    global conn
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except Error as e:
        print(e)
        Log.logging.error("In DBScript.py, OpenConnection()", exc_info=True)

'''
Retrives current DB connection
'''
def GetConnection():
    global conn
    return conn

'''
Closes connection to DB
'''
def CloseConnection():
    global conn
    conn.close()

'''
Creates table to store OSM ways data
WayID - Unique ID for a way
NodeIDs - List of Node IDs that make up the way
Street - Name of the way
'''
def CreateWaysTable():
    global conn
    qry="CREATE TABLE IF NOT EXISTS TBL_WAYS" \
        "(WayID TEXT NOT NULL," \
        "NodeIDs TEXT NOT NULL," \
        "Street VARCHAR NOT NULL," \
        "StreetPhoneticCode VARCHAR NOT NULL);"
    try:
        conn.execute(qry)
        print('Ways table created')
    except Error as e:
        print(e)
        Log.logging.error("In DBScript.py, CreateWaysTable()", exc_info=True)

'''
Table to store OpenAddresses node with its matched way
WayID - Unique ID for a way
Node - Node object data stored as string
'''
def CreateAssociatedNodesTable():
    global comm
    qry = "CREATE TABLE IF NOT EXISTS TBL_ASSOCIATED_NODES " \
          "(WayID TEXT NOT NULL," \
          "Node pickle NOT NULL);"
    try:
        conn.execute(qry)
        print('Associated nodes created')
    except Error as e:
        print(e)
        Log.logging.error("In DBScript.py, CreateAssociatedNodesTable()", exc_info=True)

'''
Query to retrieve data by matching street name from TBL_WAYS
'''
def SelectWayByStreetName(code):
    global conn
    c = conn.cursor()
    qry="SELECT * FROM TBL_WAYS WHERE StreetPhoneticCode like '%s';"%code
    try:
        c.execute(qry)
        return c.fetchall()
    except Error as e:
        print(e)
        Log.logging.error("In DBScript.py, SelectWayByStreetName()", exc_info=True)

'''
Query to insert into TBL_ASSOCIATED_NODES
'''
def InsertIntoAssociatedNodes(wayId,node):
    global conn
    c = conn.cursor()
    qry = "INSERT INTO TBL_ASSOCIATED_NODES (WayID,Node)" \
          "VALUES (?,?)"
    try:
        c.execute(qry,(wayId,node))
    except Error as e:
        print(e)
        Log.logging.error("In DBScript.py, InsertIntoAssociatedNodes()", exc_info=True)

'''
Query to insert into TBL_WAYS
'''
def InsertIntoWays(wayID,nodeIDs,street,code):
    global conn
    c = conn.cursor()
    qry = "INSERT INTO TBL_WAYS (WayID,NodeIDs,Street,StreetPhoneticCode)" \
          "VALUES('%s','%s','%s','%s');"%(wayID,nodeIDs,street,code)
    try:
        conn.execute(qry)
    except Error as e:
        print(e)
        Log.logging.error("In DBScript.py, InsertIntoWays()", exc_info=True)

def SelectDistinctWayID():
    global conn
    c = conn.cursor()
    try:
        c.execute("SELECT distinct WayID FROM TBL_ASSOCIATED_NODES;")
        return c.fetchall()
    except Error as e:
        print(e)
        Log.logging.error("In DBScript.py, SelectDistinctWayID()", exc_info=True)

def SelectAllAssociatedNodesByWayID(way):
    global conn
    c = conn.cursor()
    try:
        qry="select * from TBL_ASSOCIATED_NODES where WayID = '%s'"%(way)
        c.execute(qry)
        return c.fetchall()
    except Error as e:
        print(e)
        Log.logging.error("In DBScript.py, SelectAllAssociatedNodesByWayID()", exc_info=True)
