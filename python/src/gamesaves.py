import json
from flask_restful import Resource
from flask_restful.reqparse import RequestParser
from injector import inject
from redis import Redis
from pg import DB

class Configuration:
    def __init__(self, cache_expiration, uuid):
        self.cache_expiration = cache_expiration
        self.uuid = uuid

class GameSaveList(Resource):
    @inject
    def __init__(self, db: DB, kv: Redis, parser: RequestParser, config: Configuration):
        self.db = db
        self.kv = kv
        self.parser = parser
        self.config = config

    def post(self):
        args = self.parser.parse_args()
        gamesave = args['gamesave']
        gamesave_id = str(self.config.uuid())
        self.db.query("insert into gamesaves values ('" + gamesave_id + "', '" + gamesave + "')")       
        self.kv.set(gamesave_id, gamesave)
        self.kv.expire(gamesave_id, self.config.cache_expiration)
        return gamesave_id, 201

class GameSave(Resource):
    @inject
    def __init__(self, db: DB, kv: Redis, config: Configuration):
        self.db = db
        self.kv = kv
        self.config = config

    def get(self, gamesave_id):
        if not self.kv.expire(gamesave_id, self.config.cache_expiration):
            rows = self.db.query("select gamesave from gamesaves where id='" + gamesave_id + "'").getresult()
            if len(rows) == 0:
                return None, 404
            gamesave = rows[0].gamesave
            self.kv.set(gamesave_id, gamesave)
        else:
            gamesave = self.kv.get(gamesave_id)
        return json.loads(gamesave), 200