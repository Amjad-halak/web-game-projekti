from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/')

def index():
    return render_template('index.html')

@app.route('/game', methods=['GET', 'POST'])

def mainmenu():
    username = request.form.get('username')

    print("player:", username)

    return render_template('mainmenu.html', username=username)

if __name__ == '__main__':
    app.run(debug=True)
    