import sys
import os
sys.path.append(os.path.dirname(os.path.realpath(__file__)) + "/../src")
import common
import pymssql

def db_get(query):
    # Func db_get: Get data from DB.
    try:
        conn = pymssql.connect(host="127.0.0.1", user="sa",
                               password="1689", database="RPOS1", charset='utf8')
        cursor = conn.cursor()
        cursor.execute(query)
        res = cursor.fetchall()
        # print(res)
        conn.commit()
    except Exception as ex:
        conn.rollback()
        raise ex
    finally:
        conn.close()
    return res

res = db_get("select top 10 * from stock")

print(res)