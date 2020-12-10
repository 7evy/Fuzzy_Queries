import psycopg2
import numpy as np
from psycopg2.extensions import register_adapter, AsIs
psycopg2.extensions.register_adapter(np.int64, psycopg2._psycopg.AsIs)

def reshape(rawdata, length):
    data = []
    for e in range(len(rawdata)) :
        data.append([])
        for i in range(length):
            data[-1].append(rawdata[e][i])
    return data

ps_connection = psycopg2.connect(dbname="immo", user="root", password="occulto", host="db")
cursor = ps_connection.cursor()
cursor.execute("CREATE TABLE IF NOT EXISTS immo(id SERIAL PRIMARY KEY, type VARCHAR(12), surface REAL, pieces SMALLINT, chambres SMALLINT, loyer SMALLINT, meuble BOOLEAN, jardin BOOLEAN, terrasse BOOLEAN, dist_centre SMALLINT, dist_transport SMALLINT, dist_commerce SMALLINT);")

cursor.execute("SELECT COUNT(*) FROM immo;")
if cursor.fetchall()[0][0] == 0 :

    gendata = np.genfromtxt("db.csv", delimiter=";", dtype='S12, f8, i8, i8, i8, i8, i8, i8, i8, i8, i8')

    data = reshape(gendata, 11)

    for D in data :
        if D[0] == b'Appartement' :
            D[0] = 'Appartement'
        elif D[0] == b'Maison' :
            D[0] = 'Maison'
        else : D[0] = 'Studio'
        for k in [5, 6, 7] :
            D[k] = True if D[k] == 1 else False

        cursor.execute("INSERT INTO immo (type, surface, pieces, chambres, loyer, meuble, jardin, terrasse, dist_centre, dist_transport, dist_commerce) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);", D)
    
    print("Database filled from data/db.csv")

else : print("Database ready")

ps_connection.commit()
