import psycopg2

import schedule
import time

from datetime import date



def job():
    conn = psycopg2.connect(
        user = "postgres",
        password = "postgres",
        host = "localhost",
        port = "5432",
        database = "mydb"
    )
    cur = conn.cursor()

    sql = "UPDATE account_user SET credit_journalier = 30"
    cur.execute(sql)
    conn.commit()
    sql1 = "SELECT * FROM account_user"
    cur.execute(sql1)

    if date.today().day == 1:
        sql = "UPDATE account_user SET credit_monsuel = 300"
        cur.execute(sql)
        conn.commit()
        sql1 = "SELECT * FROM account_user"
        cur.execute(sql1)

    res1 = cur.fetchall()
    for row in res1:
            print("Id = ", row[20], )
            print("Name = ", row[21])
            print("Address  = ", row[22], "\n")
    cur.close()
    conn.close()
    print("La connexion PostgreSQL est fermée")

try:
    schedule.every().day.at("00:00").do(job)
     
except (Exception, psycopg2.Error) as error :
    print ("Erreur lors de la connexion à PostgreSQL", error)

while 1:
    schedule.run_pending()
    time.sleep(1)  
