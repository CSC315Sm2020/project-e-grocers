
import psycopg2
from config import config
 
def connect():
    """ Connect to the PostgreSQL database server """
    conn = None
    rows = []
    try:
        # read connection parameters
        params = config()
 
        # connect to the PostgreSQL server
        print('Connecting to the %s database...' % params['database'])
        conn = psycopg2.connect(**params)
        print('Connected.\n')
      
        # create a cursor
        cur = conn.cursor()
        
        # execute a statement
        print('PostgreSQL version:')
        cur.execute('SELECT version()')
 
        # display the PostgreSQL database server version
        db_version = cur.fetchone()
        print(db_version[0])
       
        # execute a query using fetchall()
        print('\nPostgreSQL SELECT result (sorted by item_name):')
        cur.execute("SELECT * FROM item")
        rows = cur.fetchall()
        print('The number of items: %d' % cur.rowcount)
        for row in rows:
            print('%s\t%s' % (row[0], row[1]))
        print('The number of customers: %d' % cur.rowcount)
        for row in rows:
            print('%s\t%s' % (row[0], row[1]))



       # close the communication with the PostgreSQL
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
            print('\nDatabase connection closed.')
 
if __name__ == '__main__':
    connect()
