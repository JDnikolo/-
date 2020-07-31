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
app.url_map.strict_slashes = False #ignore trailing slashes

# enable CORS
CORS(app, resources={r'/*': {'origins': '*'}})

#sanity check page
@app.route('/')
def hello_world():
    return render_template('index.html')

##Deprecated, use signup and login instead!
@app.route('/accounts', methods=['GET', 'POST'])    
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
        data=request.get_json() 
        data['created']=time.strftime('%Y-%m-%dT%H:%M:%SZ',time.gmtime())
        data['modified']=time.strftime('%Y-%m-%dT%H:%M:%SZ',time.gmtime())
        mongo.db.Accounts.insert_one(data)
        return json.dumps({'success':True}), 200, {'ContentType':'application/json'} 

#signs up a user. The request data should be a json containing
#the user's username and password.
@app.route('/signup', methods=['POST'])    
def signup(): 
    data=request.get_json()
    account=list(mongo.db.Accounts.find({'username': data['username']}))
    if account==[]:
        data['created']=time.strftime('%Y-%m-%dT%H:%M:%SZ',time.gmtime())
        data['modified']=time.strftime('%Y-%m-%dT%H:%M:%SZ',time.gmtime())
        mongo.db.Accounts.insert_one(data)
        return json.dumps({'success':True}), 200, {'ContentType':'application/json'}
    else:
        return json.dumps({'success':False}), 400, {'ContentType':'application/json'} 

#logs in a user. The request should contain the user's
#username and password.
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

#changes a user's password. The request should contain the user's
#username, old password (oldPassword) and new password (newPassword)
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

#Returns all studies (condition-drugs entries) for a certain drug or certain 
# condition, or all studies if unspecified.
##deprecated, only for administrative use! Use conditionList instead.
@app.route('/studies') 
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

#returns all drugs used for a given condition sorted by the
#number of studies they were used in.
@app.route('/condition') ##main functionality
def condition():
	condition=request.args.get('condition')
	pipeline = [{"$match":{"condition":condition }},{"$unwind": "$drugs"}, {"$group": {"_id": "$drugs", "count": {"$sum": 1}}}, {"$sort": SON([("count", -1), ("_id", -1)])}]
	sortedResults = list(mongo.db.Studies.aggregate(pipeline))
	#pprint(sortedResults)
	return json.dumps(sortedResults,default=str)

#Returns a list with an amount of conditions specified by size and offset by page.
#The conditions are not sorted.
@app.route('/conditionlist')
def conditionlist():
    try:
        page=int(request.args.get('page'))
        size=int(request.args.get('size'))
    except TypeError:
        size=56750
        page=0
    if page==None:
        page=0
    if size==None:
        size=56750
    conditions=(list(mongo.db.Studies.aggregate([{"$group":{"_id":"$condition"}},{"$project":{"_id":0,"condition":"$_id"}},{ "$skip": page*size },{ "$limit": size}])))
    return json.dumps(conditions,default=str)


#Main score handling endpoint. Returns all scores of a user, all scores
#on a condition, or all scores.
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

#Autocomplete support endpoint. Returns all studies that contain the 
#substring term.
@app.route('/autocomplete')
def autocomplete():
    term=request.args.get('term')
    if term!=None:
        conditions=list(mongo.db.Studies.aggregate(([{"$match": {"condition": {"$regex": ".*"+term+".*"}}}, {"$group":{"_id":"$condition"}},{"$project":{"_id":0,"condition":"$_id"}}])))
        return json.dumps(conditions, default=str)

if __name__ == '__main__':
    app.run()
