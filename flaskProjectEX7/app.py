from flask import Flask, redirect, url_for

app = Flask(__name__)

@app.route('/')
def main():
    return 'Welcome to main page-Web course'

@app.route('/whatsUp')
def about1():
    return 'Wanna hear a joke? Bill Gates got divorced, but it isnt too bad because when god closes doors, he opens windows ;)'

@app.route('/hello')
def hello():
    return redirect('/whatsUp')


@app.route('/backTo')
def goToMain():
 return redirect(url_for('main'))


if __name__ == '/main':
    app.run(debug=True)