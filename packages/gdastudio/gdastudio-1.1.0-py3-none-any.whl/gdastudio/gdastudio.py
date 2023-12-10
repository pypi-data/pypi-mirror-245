# KAMIL MARTENCZUK 15.08.2022
# FULL ACCESS TO DB TABLES VIEWS AND SCALAR FUNCTION
import json
import csv
import pypyodbc
from tqdm import tqdm
from colorama import init, Fore, Style, Back
import psycopg2 as p2

class JSONFile:
    def __init__(self, path, name) -> object:
        self.filepath = path
        self.filename = name
        self.data = json.load(open(self.filepath + '/' + self.filename + '.json'))

class CSVFile:
    def __init__(self, path, name, delimiter) -> object:
        self.filepath = path
        self.filename = name
        self.delim = delimiter
        self.data = csv.reader(open(self.filepath + '/' + self.filename + '.csv', mode='r'), delimiter=self.delim)
        self.array = [x for x in self.data]

class SQLConn:
    def __init__(self, configFile: JSONFile) -> object:
        self.drivers = configFile.data['drivers']
        self.server = configFile.data['server']
        self.port = configFile.data['port']
        self.user = configFile.data['user']
        self.password = configFile.data['password']
        self.database = configFile.data['database']
        self.trustmode = configFile.data['Trusted_Connection']
        self.conn = pypyodbc.connect('DRIVER={' + self.drivers + '};SERVER='+ self.server +';UID='+ self.user +';PWD='+ self.password +';DATABASE='+ self.database +';Trusted_Connection='+ self.trustmode +';')

class SQLObject:
    def __init__(self, schemaName, objectName) -> object:
        self.schema = "[" + schemaName + "]"
        self.object = "[" + objectName + "]"
        self.fullname = self.schema + "." + self.object

class SQLConnectionPG:
    def __init__(self, SQLServer) -> object:
        self.host = SQLServer.host
        self.database = SQLServer.database
        self.user = SQLServer.user
        self.password = SQLServer.password
        self.conn = p2.connect(host=self.host, database=self.database, user=self.user, password=self.password)

class SQLConnectionSQLServer:
    def __init__(self, SQLServerJSONpath, SQLServerJSONfilename) -> object:
        self.path = SQLServerJSONpath
        self.filename = SQLServerJSONfilename
        self.conn = SQLConn(JSONFile(self.path, self.filename)).conn

class SQLServer:
    def __init__(self, host, database, user, password) -> object:
        self.host = host
        self.database = database
        self.user = user
        self.password = password

class SQLSelect:
    def __init__(self, SQLConnection, SQLTable, Count, IndexOrderBy, ASCmode) -> object:
        self.conn = SQLConnection
        self.cursor = self.conn.cursor()
        self.table = SQLTable
        self.count = Count
        self.index = IndexOrderBy
        self.ascmode = ASCmode
        self.cursor.execute(
            "Select * from " + self.table.schema + "." + self.table.name + " ORDER BY " +self.index+" "+self.ascmode+" FETCH FIRST " + self.count + " ROWS ONLY")
        self.data = self.cursor.fetchall()

class SQLTable:
    def __init__(self, schema, name) -> object:
        self.schema = schema
        self.name = name

def VTE(source: SQLObject, destination: SQLObject, SQLConnection: SQLConn):
    init(autoreset = True)
    print(Style.DIM + Back.WHITE + Fore.BLACK + "\n SQL View " + source.fullname + " is converted to SQL Table " + destination.fullname + " in database " + SQLConnection.database + "  " + Fore.CYAN + Back.BLACK + "\n\n   Please Stand By...\n")
    conn0 = SQLConnection.conn
    cursor = conn0.cursor()
    cols = cursor.execute("""Select [name] from sys.columns WHERE object_id = OBJECT_ID('"""+source.fullname+"""')""").fetchall()
    cols_string = cols[0][0]
    try:
        for i in range (1,len(cols)): cols_string += " , [" + cols[i][0] + "]"
        rows = cursor.execute("""Select ["""+cols[0][0]+"""] from """+source.fullname+""" ORDER BY date""").fetchall()
        for i in tqdm(range(len(rows))):
            row = cursor.execute("""Select * from """+source.fullname+""" WHERE """+cols[0][0]+"""='"""+rows[i][0]+"""'""").fetchall()
            values_string = "'" + row[0][0] + "'"
            for j in range (1,len(row[0])): values_string += ",'" + str(row[0][j])+"'"
            try: cursor.execute(""" Insert into """ + destination.fullname + """ (""" + cols_string + """) VALUES (""" + values_string + """)""")
            except: pass
            cursor.commit()
        print(Fore.GREEN + " \n Success \n ")
    except: print(Fore.RED + " \n Error \n ")
    conn0.close()
    return 0

def CTE(source: CSVFile, destination: SQLObject, SQLConnection: SQLConn):
    init(autoreset = True)
    print(Style.DIM + Back.WHITE + Fore.BLACK + "\n CSV file " + source.filename + ".csv is exported to SQL Table " + destination.fullname + " in database " + SQLConnection.database + "  " + Fore.CYAN + Back.BLACK + "\n\n   Please Stand By...\n")
    CSV_arr = source.array
    col_string = "[" + CSV_arr[0][0] + "]"
    for i in range (1,len(CSV_arr[0])):
        if CSV_arr[0][i] == "":
            print(Fore.RED + " \n File is empty or check columns \n ")
            return 0
        col_string += " , [" + CSV_arr[0][i] +"]"
    conn0 = SQLConnection.conn
    cursor = conn0.cursor()
    cols_SQL = cursor.execute("""Select [name] from sys.columns WHERE object_id = OBJECT_ID('"""+destination.fullname+"""')""").fetchall()
    cols_SQL_string = "[" + cols_SQL[0][0] +"]"
    try:
        for i in range (1,len(cols_SQL)): cols_SQL_string += " , [" + cols_SQL[i][0] + "]"
        if cols_SQL_string != col_string:
            print(Fore.RED + " \n Columns in file and in database are different \n ")
            return 0
        else:
            for i in tqdm(range(len(CSV_arr)-1)):
                values_string = "'" + CSV_arr[i+1][0] + "'"
                for j in range (1,len(CSV_arr[i])): values_string += ",'" + str(CSV_arr[i+1][j])+"'"
                try: cursor.execute(""" Insert into """ + destination.fullname + """ (""" + col_string + """) VALUES (""" + values_string + """)""")
                except: pass
                cursor.commit()
            print(Fore.GREEN + " \n Success \n ")
    except: print(Fore.RED + " \n Error \n ")
    conn0.close()
    return 0

class CursorManager:
    def __init__(self, config):
        self.db_type = config['db_type']
        self.config = { key: value for key, value in config.items() if key != "db_type"}
        
    def __enter__(self):
        match(self.db_type):
            case "PGSQL":
                self.conn = p2.connect(**self.config)

            case "MSSQL":
                self.conn = pypyodbc.connect(**self.config)

            case _:
                raise("UKNOWN_DB_TYPE")

        self.curs = self.conn.cursor()
        return self.curs
     
    def __exit__(self, exc_type, exc_value, exc_traceback):
        self.conn.commit()
        self.curs.close()
        self.conn.close()

class PostgreSql:
    def __init__(self, config):
        self.config = config
        
    def __enter__(self):
        self.conn = p2.connect(**self.config)
        self.curs = self.conn.cursor()
        return self.curs
     
    def __exit__(self, exc_type, exc_value, exc_traceback):
        self.conn.commit()
        self.curs.close()
        self.conn.close()


def rows_to_dicts(cursor):
    headers = [header[0] for header in cursor.description]
    rows = cursor.fetchall()
    return [
        {header: row[index] for (index, header) in enumerate(headers)}
        for row in rows
    ]


def row_to_dict(cursor):
    headers = [header[0] for header in cursor.description]
    row = cursor.fetchone()
    return {
        header: row[index] 
        for (index, header) in enumerate(headers)
    } if row else None


def columns_to_dict(cursor):
    headers = [header[0] for header in cursor.description]
    rows = cursor.fetchall()
    return {
        header: [row[index] for row in rows]
        for (index, header) in enumerate(headers)
    }


def row_to_value(cursor):
    row = cursor.fetchone()
    return row[0] if row else None

def ver(): print('1.1.0')