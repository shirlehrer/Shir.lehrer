from flask import Flask, render_template, request

app = Flask(__name__)


@app.route('/')
def home():
    return render_template('CV.html')


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

if __name__ == '__main__':
    app.run(debug=True)
