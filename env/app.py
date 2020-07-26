from flask import Flask, jsonify, request
from flask import render_template
from flask import redirect, url_for
from flask_cors import CORS
from flask_pymongo import PyMongo
from bson import json_util
import json
from pprint import pprint
from bson.son import SON
import time

# instantiate the app
app = Flask(__name__)
# setup mongo
app.config["MONGO_URI"] = "mongodb://localhost:27017/local"
mongo = PyMongo(app)


# configuration
DEBUG = True
app.config.from_object(__name__)
app.url_map.strict_slashes = False

# enable CORS
CORS(app, resources={r'/*': {'origins': '*'}})


@app.route('/')
def hello_world():
    return render_template('index.html')


@app.route('/accounts', methods=['GET', 'POST'])    ##Deprecated, use signup instead!
def accounts():
    if request.method=='GET':
        username = request.args.get('username')
        if username != None:
            account = mongo.db.Accounts.find_one({'username': username})
            if account == None:
                return json.dumps({})
            return json.dumps(account, default=str)
        else:
            accounts = list(mongo.db.Accounts.find())
            return json.dumps(accounts, default=str)
    elif request.method=='POST':  
        data=request.get_json()     #TODO Add check if account with requested username exists!!!
        data['created']=time.strftime('%Y-%m-%dT%H:%M:%SZ',time.gmtime())
        data['modified']=time.strftime('%Y-%m-%dT%H:%M:%SZ',time.gmtime())
        mongo.db.Accounts.insert_one(data)
        return json.dumps({'success':True}), 200, {'ContentType':'application/json'} 

@app.route('/signup', methods=['POST'])    ##
def signup(): 
    data=request.get_json()     #TODO Add check if account with requested username exists!!!
    data['created']=time.strftime('%Y-%m-%dT%H:%M:%SZ',time.gmtime())
    data['modified']=time.strftime('%Y-%m-%dT%H:%M:%SZ',time.gmtime())
    mongo.db.Accounts.insert_one(data)
    return json.dumps({'success':True}), 200, {'ContentType':'application/json'} 

@app.route('/login',methods=['POST'])
def login():
    data=request.get_json()  
    if data['username'] != None and data['password']!=None:
        account = mongo.db.Accounts.find_one({'username': data['username']})
        if account == None:
            return json.dumps({'success':False}), 403, {'ContentType':'application/json'}
        if data['password']==account['password']:
            mongo.db.Accounts.update_one(account, {"$set":{"lastLogin": time.strftime('%Y-%m-%dT%H:%M:%SZ',time.gmtime())}})
            return json.dumps({'success':True}), 200, {'ContentType':'application/json'}
    return json.dumps({'success':False}), 403, {'ContentType':'application/json'}     

@app.route('/changePassword',methods=['POST'])
def changePassword():
    data=request.get_json()  
    if data['username'] != None and data['oldPassword']!=None and data['newPassword']!=None:
        account = mongo.db.Accounts.find_one({'username': data['username']})
        if account == None:
            return json.dumps({'success':False}), 403, {'ContentType':'application/json'}
        if data['oldPassword']==account['password']:
            mongo.db.Accounts.update_one(account, {"$set":{"modified": time.strftime('%Y-%m-%dT%H:%M:%SZ',time.gmtime()),"password":data['newPassword']}})
            return json.dumps({'success':True}), 200, {'ContentType':'application/json'}
    return json.dumps({'success':False}), 403, {'ContentType':'application/json'} 

@app.route('/studies') ##deprecated, only for administrative use(?)
def studies():
    condition = request.args.get('condition')
    drug = request.args.get('drug')
    if drug != None:
        drugs = list(mongo.db.Studies.find({"drugs": drug}))
        return json.dumps(drugs, default=str)
    if condition != None:
        conditions = list(mongo.db.Studies.find({"condition": condition}))
        return json.dumps(conditions, default=str)
    else:
        accounts = list(mongo.db.Studies.find())
        return json.dumps(accounts, default=str)


@app.route('/condition') ##main functionality
def condition():
	condition=request.args.get('condition')
	pipeline = [{"$match":{"condition":condition }},{"$unwind": "$drugs"}, {"$group": {"_id": "$drugs", "count": {"$sum": 1}}}, {"$sort": SON([("count", -1), ("_id", -1)])}]
	sortedResults = list(mongo.db.Studies.aggregate(pipeline))
	#pprint(sortedResults)
	return json.dumps(sortedResults,default=str)


@app.route('/conditionlist')
def conditionlist():
    page=int(request.args.get('page'))      ##TODO add try-catch failsafes!
    size=int(request.args.get('size'))
    if page==None:
        page=0
    if size==None:
        size=0
    conditions=(list(mongo.db.Studies.aggregate([{"$group":{"_id":"$condition"}},{"$project":{"_id":0,"condition":"$_id"}},{ "$skip": page*size },{ "$limit": size}])))
    return json.dumps(conditions,default=str)



@app.route('/scores' ,methods=['GET', 'POST'])
def scores():
    if request.method=='GET':
        condition = request.args.get('condition')
        username = request.args.get('username')
        if username != None:
            username = list(mongo.db.Scores.find({"username": username}))
            return json.dumps(username, default=str)
        if condition != None:
            conditions = list(mongo.db.Scores.find({"condition": condition}))
            return json.dumps(conditions, default=str)
        else:
            accounts = list(mongo.db.Scores.find())
            return json.dumps(accounts, default=str)
    elif request.method=='POST':
        data=request.get_json()
        #pprint(data)
        mongo.db.Scores.insert_one(data)
        return json.dumps({'success':True}), 200, {'ContentType':'application/json'} 



if __name__ == '__main__':
    app.run()
