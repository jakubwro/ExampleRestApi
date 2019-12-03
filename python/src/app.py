from flask import Flask
from flask_restful import reqparse, abort, Api, Resource
from flask_restful.reqparse import RequestParser
from flask_injector import FlaskInjector, request
from injector import inject
from redis import Redis
from pg import DB
from uuid import uuid4

from gamesaves import Configuration, GameSave, GameSaveList

app = Flask(__name__)
api = Api(app)

api.add_resource(GameSaveList, '/gamesaves/')
api.add_resource(GameSave, '/gamesaves/<gamesave_id>')

def configure(binder):
    parser = RequestParser()
    parser.add_argument('gamesave')
    binder.bind(RequestParser, to=parser, scope=request)
    binder.bind(DB, to=DB(host='db', user="postgres", passwd="zaq12wsx", dbname="api_storage"), scope=request)
    binder.bind(Redis, to=Redis(host='kvs', port=6379, db=0), scope=request)
    binder.bind(Configuration, to=Configuration(2*24*60*60, uuid4), scope=request)
        
FlaskInjector(app=app, modules=[configure])

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=3000)
