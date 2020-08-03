from flask import Flask,render_template,request,Response,flash,redirect,url_for,jsonify,abort
app = Flask(__name__)
@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
