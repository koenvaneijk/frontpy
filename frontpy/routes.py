from flask import Flask, render_template, send_file

app = Flask(__name__)

@app.route("/")
def hello():
    return render_template('app.html')

@app.route('/frontend')
def frontend():
    return send_file('./frontend.py')

@app.route('/ui')
def ui():
    return send_file('./ui.py')

if __name__ == "__main__":
    app.run(debug=True, port=8080)