from flask import Flask
from flask import render_template
from flask import redirect,url_for
from flask_cors import CORS

app = Flask(__name__)

# configuration
DEBUG = True

# instantiate the app
app = Flask(__name__)
app.config.from_object(__name__)

# enable CORS
CORS(app, resources={r'/*': {'origins': '*'}})

@app.route('/')
def hello_world(): 
    return render_template('index.html')

if __name__ == '__main__':
    app.run()