from flask import Flask, render_template, url_for, session, request, redirect, jsonify
import mysql.connector

app = Flask(__name__)
app.secret_key = '1308'

contacts = {'WinnieThePooh': {'email': 'winnie.pooh@disney.in', 'first_name': 'Winnie', 'last_name': 'the pooh'},
            'MickeyMouse': {'email': 'mickey.mouse@disney.in', 'first_name': 'Mickey', 'last_name': 'Mouse'},
            'Donald': {'email': 'donald@disney.in', "first_name": 'Donald', 'last_name': 'duck'},
            'Piglet': {'email': 'piglet@disney.in', "first_name": 'Piglet', 'last_name': 'the pig'},
            'Roo': {'email': 'roo@disney.in', "first_name": 'Roo', 'last_name': 'the kangeroo'}}


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


@app.route('/')
def home():
    return render_template('CV.html')


@app.route('/assignment9', methods=['GET', 'POST'])
def assignment9():
    if request.method == 'GET':
        if request.args:
            if 'username' in request.args:
                if request.args['username'] == '':
                    return render_template('assignment9.html', didsearch=True, users=contacts)
                elif request.args['username'] != '':
                    if request.args['username'] in contacts:
                        return render_template('assignment9.html', found=True, didsearch=True,
                                               username=request.args['username'],
                                               users=contacts[request.args['username']])
                    else:
                        return render_template('assignment9.html', found=False, didsearch=True)
            else:
                return render_template('assignment9.html', didsearch=False)
        else:
            return render_template('assignment9.html')
    elif request.method == 'POST':
        if request.form['username'] in contacts:
            session['username'] = request.form['username']
            session['logged_in'] = True
            return render_template('assignment9.html')
        else:
            contacts[request.form['username']] = {'email': request.form['email'],
                                                  'first_name': request.form['first_name'],
                                                  'last_name': request.form['last_name']}
            session['username'] = request.form['username']
            session['logged_in'] = True
            return render_template('assignment9.html')


@app.route('/logout', methods=['GET', 'POST'])
def logout():
    contacts[session['username']] = {'email': '', 'first_name': '', 'last_name': ''}
    session['logged_in'] = False
    return redirect(url_for('assignment9'))


@app.route('/assignment8')
def assignment8():
    name = 'Arseni'
    day = 'SomeDay'
    song = 'A whole new world', 'Intro', 'Aint no sunshine'
    return render_template('assignment8.html',
                           name=name,
                           day=day,
                           songs=song)


@app.route('/favorite')
def favorite():
    name = 'Arseni'
    day = 'SomeDay'
    return render_template('favorite.html',
                           name=name,
                           day=day)


@app.route('/contactlist')
def contactlist():
    return render_template('contact list.html')


from flaskProject.assignment10.assignment10 import assignment10

app.register_blueprint(assignment10)


# ------------ex11-----------#
@app.route('/assignment11/users', methods=['get'])
def ex11():
    query = "SELECT * FROM userss "
    query_result = interact_db(query, query_type='fetch')
    return jsonify(users=query_result)


@app.route('/assignment11/users/selected/', defaults={'SOME_USER_ID': 5})
@app.route('/assignment11/users/selected/<int:SOME_USER_ID>')
def get_user(SOME_USER_ID=None):
    if SOME_USER_ID:
        query = "SELECT * FROM userss WHERE id='%s'" % SOME_USER_ID
        query_result = interact_db(query, query_type='fetch')
        if len(query_result) != 0:
            return jsonify(query_result)
    return jsonify({'success': False,
                    'error': 'Request failed'})


if __name__ == '__main__':
    app.run(debug=True)
