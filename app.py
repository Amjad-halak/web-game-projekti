from flask import Flask, render_template, request, session

app = Flask(__name__, template_folder='static')
app.secret_key = "ripuli"

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/menu', methods=['POST', 'GET'])
def mainmenu():
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        if username:
            session['username'] = username
    return render_template('mainmenu.html')

if __name__ == '__main__':
    app.run(debug=True)
    