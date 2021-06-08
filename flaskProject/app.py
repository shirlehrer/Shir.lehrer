from flask import Flask, render_template, url_for, session, request, redirect, Blueprint


app = Flask(__name__)
app.secret_key = '1308'

contacts = {'WinnieThePooh': {'email': 'winnie.pooh@disney.in', 'first_name': 'Winnie', 'last_name': 'the pooh'},
           'MickeyMouse': {'email': 'mickey.mouse@disney.in', 'first_name': 'Mickey','last_name': 'Mouse'},
           'Donald': {'email': 'donald@disney.in', "first_name": 'Donald', 'last_name': 'duck'},
           'Piglet': {'email': 'piglet@disney.in', "first_name": 'Piglet', 'last_name': 'the pig'},
           'Roo': {'email': 'roo@disney.in', "first_name": 'Roo', 'last_name': 'the kangeroo'}}

@app.route('/')
def home():
    return render_template('CV.html')

@app.route('/assignment9', methods=['GET','POST'])
def assignment9():
    if request.method == 'GET':
        if request.args:
            if 'username' in request.args:
                if request.args['username'] == '':
                    return render_template('assignment9.html', didsearch=True, users=contacts)
                elif request.args['username'] != '':
                    if request.args['username'] in contacts:
                        return render_template('assignment9.html', found=True, didsearch=True,
                                               username=request.args['username'], users=contacts[request.args['username']])
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


if __name__ == '__main__':
    app.run(debug=True)


