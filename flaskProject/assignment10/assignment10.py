from flask import Flask, render_template, request, redirect, Blueprint, flash
import mysql.connector

app = Flask(__name__)
app.secret_key = '1308'

assignment10 = Blueprint('assignment10', __name__,
                         static_folder='static',
                         static_url_path='/assignment10',
                         template_folder='templates')


def interact_db(query, query_type: str):
    return_value = False
    connection = mysql.connector.connect(host='localhost',
                                         user='root',
                                         password='root',
                                         database='assignment10')
    cursor = connection.cursor(named_tuple=True)
    cursor.execute(query)

    if query_type == 'commit':  # change DB
        connection.commit()
        return_value = True
    if query_type == 'fetch':  # read DB
        query_result = cursor.fetchall()
        return_value = query_result

    connection.close()
    cursor.close()
    return return_value


# -----------select------------------ #
@assignment10.route('/assignment10')
def users():
    query = "select * from users"
    query_result = interact_db(query=query, query_type='fetch')
    return render_template('assignment10.html', users=query_result)


# -------------insert---------------- #
@assignment10.route('/insert', methods=['GET', 'POST'])
def insert_users():
    if request.method == 'POST':
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        email = request.form['email']
        username = request.form['username']
        check = "SELECT username FROM users WHERE username='%s';" % username
        lenCheck = interact_db(query=check, query_type='fetch')
        if username == '' or first_name == '' or last_name == '' or email == '':
            flash('PLEASE FILL ALL FIELDS!')
            return redirect('/assignment10')
        else:
            if len(lenCheck) == 0:
                query = "INSERT INTO users(username, email, first_name, last_name) VALUES ('%s', '%s', '%s', '%s');" \
                        % (username, email, first_name, last_name)
                interact_db(query=query, query_type='commit')
                flash('A new user was inserted to DB')
                return redirect('/assignment10')
            else:
                flash('User requested already exists in DB')
                return redirect('/assignment10')
    return render_template('assignment10.html', req_method=request.method)


# -------------delete---------------- #
@assignment10.route('/delete', methods=['POST'])
def delete_users():
    username = request.form['username']
    check = "SELECT username FROM users WHERE username='%s';" % username
    lenCheck = interact_db(query=check, query_type='fetch')
    if len(lenCheck) != 0:
        query = "DELETE FROM users WHERE username='%s';" % username
        interact_db(query=query, query_type='commit')
        flash('User was deleted from DB')
        return redirect('/assignment10')
    elif len(lenCheck) == 0:
        flash('User requested does not exist in DB')
        return redirect('/assignment10')


# -------------update---------------- #
@assignment10.route('/update', methods=['GET', 'POST'])
def update():
    if request.method == 'POST':
        username = request.form['username']
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        email = request.form['email']
        if username == '' or first_name == '' or last_name == '' or email == '':
            flash('PLEASE FILL ALL FIELDS!')
            return redirect('/assignment10')
        else:
            check = "SELECT username FROM users WHERE username='%s';" % username
            lenCheck = interact_db(query=check, query_type='fetch')
            if len(lenCheck) != 0:
                query = "UPDATE users SET first_name='%s', last_name='%s', email='%s' WHERE username='%s';" % \
                        (first_name, last_name, email, username)
                interact_db(query=query, query_type='commit')
                flash('User was updated in DB')
                return redirect('/assignment10')
            elif len(lenCheck) == 0:
                flash('User requested does not exist in DB')
                return redirect('/assignment10')
