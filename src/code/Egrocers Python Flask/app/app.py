# importing config , library
import psycopg2
from config import config
from flask import Flask, render_template, request, flash, redirect, url_for


def connect(query):
    """ Connect to the PostgreSQL database server """
    conn = None
    rows = []
    try:
        # read connection parameters
        params = config()

        # connect to the PostgreSQL server
        print('Connecting to the %s database...' % (params['database']))
        conn = psycopg2.connect(**params)
        print('Connected.')

        # create a cursor
        cur = conn.cursor()

        # execute a query using fetchall()
        cur.execute(
            "SELECT * from  item  WHERE item_type = '%s'" % query)
        rows = cur.fetchall()

       # close the communication with the PostgreSQL
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
            print('Database connection closed.')
    # return the query result from fetchall()
    return rows

# for employee information


def connectview(employeedata):
    """ Connect to the PostgreSQL database server """
    conn = None
    rows = []
    try:
        # read connection parameters
        params = config()

        # connect to the PostgreSQL server
        print('Connecting to the %s database...' % (params['database']))
        conn = psycopg2.connect(**params)
        print('Connected.')

        # create a cursor
        cur = conn.cursor()

        # execute a query using fetchall()
        cur.execute("select * from employee")
        rows = cur.fetchall()

       # close the communication with the PostgreSQL
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
            print('Database connection closed.')
    # return the query result from fetchall()
    return rows


# connect sale for sales data
def connectsale(sales):
    """ Connect to the PostgreSQL database server """
    conn = None
    rows = []
    try:
        # read connection parameters
        params = config()

        # connect to the PostgreSQL server
        print('Connecting to the %s database...' % (params['database']))
        conn = psycopg2.connect(**params)
        print('Connected.')

        # create a cursor
        cur = conn.cursor()

        # execute a query using fetchall()
        cur.execute(
            "select customername, custid, itemno, quantity from customer natural join sale")
        rows = cur.fetchall()

       # close the communication with the PostgreSQL
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
            print('Database connection closed.')
    # return the query result from fetchall()
    return rows

# insert an item
def connectAdd(item_name, itemno, item_type, item_price, aisle):
    """ Connect to the PostgreSQL database server """
    conn = None
    rows = []
    try:
        # read connection parameters
        params = config()

        # connect to the PostgreSQL server
        print('Connecting to the %s database...' % (params['database']))
        conn = psycopg2.connect(**params)
        print('Connected.')

        # create a cursor
        cur = conn.cursor()

        # execute a query using fetchall()
        cur.execute("INSERT INTO ITEM(item_name, itemno, item_type, item_price, aisle) VALUES (%s, %s,%s,%s,%s))",
                    item_name, itemno, item_type, item_price, aisle)
        count = cur.rowcount()
        conn.commit()
        print(count, "Record added succefully to the database")
        rows = cur.fetchall()

       # close the communication with the PostgreSQL
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
            print('Database connection closed.')
    # return the query result from fetchall()
    return rows

# deleting an item from database


def connectDelete(item_name, itemno, item_type, item_price, aisle):
    """ Connect to the PostgreSQL database server """
    conn = None
    rows = []
    try:
        # read connection parameters
        params = config()

        # connect to the PostgreSQL server
        print('Connecting to the %s database...' % (params['database']))
        conn = psycopg2.connect(**params)
        print('Connected.')

        # create a cursor
        cur = conn.cursor()

        # execute a query using fetchall()
        cur.execute("DELETE FROM ITEM WHERE Itemno = '%s'", itemno)
        conn.commit()
        print("Record deleted  succefully from the database")
        rows = cur.fetchall()

       # close the communication with the PostgreSQL
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
            print('Database connection closed.')
    # return the query result from fetchall()
    return rows

#view the final item
def connectFinalView(finalView):
    """ Connect to the PostgreSQL database server """
    conn = None
    rows = []
    try:
        # read connection parameters
        params = config()

        # connect to the PostgreSQL server
        print('Connecting to the %s database...' % (params['database']))
        conn = psycopg2.connect(**params)
        print('Connected.')

        # create a cursor
        cur = conn.cursor()

        # execute a query using fetchall()
        cur.execute("select * from item order by itemno, item_type, item_price, item_name, brand_name, aisle")
        conn.commit()
        print("Records in the database ")
        rows = cur.fetchall()

       # close the communication with the PostgreSQL
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
            print('Database connection closed.')
    # return the query result from fetchall()
    return rows


# app.py

app = Flask(__name__)


# serve form web page
@app.route("/")
def form():
    return render_template('my-form.html')

# handle form data
@app.route('/form-handler', methods=['POST'])
def handle_data():
    query = request.form['query']
    rows = connect(query)
    if query == '':
        return render_template('my-form.html', message='Please enter required fields')
    return render_template('my-result.html', rows=rows)


# display data
@app.route('/form-view', methods=['POST'])
def view_data():
    rows = connectview(request.form['employeedata'])
    return render_template('my-result.html', rows=rows)

# display sales


@app.route('/form-sale', methods=['POST'])
def customer_data():
    rows = connectsale(request.form['sales'])
    return render_template('my-result.html', rows=rows)

# adding an item


@app.route('/form-adder', methods=['POST'])
def item_adder():
    flash("Item added Successfully")
    item_name = request.form['item_name']
    itemno = request.form['itemno']
    item_type = request.form['item_type']
    item_price = request.form['item_price']
    aisle = request.form['aisle']
    rows = connectAdd(item_name, itemno, item_type, item_price, aisle)
    if item_name == '' or itemno == '' or item_type == '' or item_price == '':
        return render_template('my-form.html', message='Please enter required fields')
    return render_template('updated.html', rows=rows)

# delete item


@app.route('/form-delete', methods=['POST'])
def delete_Item():
    item_name = request.form['item_name']
    itemno = request.form['itemno']
    item_type = request.form['item_type']
    item_price = request.form['item_price']
    aisle = request.form['aisle']
    rows = connectDelete(item_name, itemno, item_type, item_price, aisle)
    flash(item_name, "Item Deleted successfully")
    return render_template('removed.html', rows=rows)

@app.route('/final-view', methods=['POST'])
def results():
    all = request.form['all']
    rows =connectFinalView(all)
    return render_template('allitem.html', rows = rows)

if __name__ == '__main__':
    app.secret_key = 'super secret key'
    app.config['SESSION_TYPE'] = 'filesystem'

    app.run(debug=True)
