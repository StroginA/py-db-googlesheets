import psycopg2
from fetch_sheets import fetch
import time


def main():
    """
    Fetches rows from Google Sheets table.
    Fetches data from DB.
    Deletes rows from DB if they no longer exist in Sheets.
    Updates rows where orderId matches.
    Inserts rows where orderId does not match.
    """
    sheets_rows = fetch()
    sheets_idx = [row[0] for row in sheets_rows]
    insert_or_update_sql = """
    UPDATE db_order SET
        "costUSD" = %s,
        "costRUB" = %s,
        "deliveryDate" = %s
    WHERE
        "db_order"."orderId" = %s;

    INSERT INTO db_order (
        "orderId",
        "costUSD",
        "costRUB",
        "deliveryDate")
    SELECT %s, %s, %s, %s
    WHERE NOT EXISTS (SELECT "orderId" FROM db_order WHERE "orderId" = %s);
    """
    select_sql = """SELECT * FROM db_order;"""
    truncate_sql = """TRUNCATE TABLE db_order;"""
    select_idx_sql = """SELECT "orderId" from db_order;"""
    delete_sql = """DELETE FROM db_order WHERE "orderId"=%s"""
    conn = None
    try:
        # connect to the PostgreSQL database
        conn = psycopg2.connect(
            host="localhost",
            database="ksdb",
            user="ksuser",
            password="kspass")
        # create a new cursor
        cur = conn.cursor()
        cur.execute(select_idx_sql)
        # deletes entries if they are not in Sheets
        idx = [el[0] for el in cur.fetchall()]
        to_delete = [id for id in idx if id not in sheets_idx]
        for id in to_delete:
            cur.execute(delete_sql, (id,))
        for row in sheets_rows:
            orderId, costUSD, costRUB, deliveryDate = row
            cur.execute(insert_or_update_sql, (
                costUSD, 
                costRUB, 
                deliveryDate, 
                orderId, 
                orderId,
                costUSD, 
                costRUB, 
                deliveryDate,
                orderId))

        # Commit the changes to the database
        conn.commit()
        # Close communication with the PostgreSQL database
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()



if __name__ == '__main__':
    while True:
        # runs every 30 seconds
        main()
        time.sleep(30)