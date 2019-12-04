import unittest
import json
from unittest.mock import MagicMock

from gamesaves import Configuration, GameSave, GameSaveList

class Object(object):
    pass

class GameSaveResourceTest(unittest.TestCase):
    def test_retrieving_gamestate_when_cache_hit(self):
        gamesave_id = "11111111-2222-1111-2222-000000000000"
        gamesave = {}
        cache_expiration = 999

        db = Object()
       
        kv = Object()
        kv.expire =  MagicMock(return_value=True)
        kv.get = MagicMock(return_value=str(gamesave))

        config = Configuration(cache_expiration, lambda: gamesave_id)
        
        cut = GameSave(db, kv, config)
        (result, status) = cut.get(gamesave_id)

        self.assertEqual(result, gamesave)
        self.assertEqual(status, 200)
        kv.expire.assert_called_with(gamesave_id, cache_expiration)
        kv.expire.get(gamesave_id)

    def test_retrieving_gamestate_when_cache_miss(self):
        gamesave_id = "11111111-2222-1111-2222-000000000000"
        gamesave = "{}"
        cache_expiration = 999

        db = Object()
        row = (gamesave,)
        queryresult = Object()
        queryresult.getresult = MagicMock(return_value=[row])
        db.query = MagicMock(return_value=queryresult)
       
        kv = Object()
        kv.expire =  MagicMock(return_value=False)
        kv.set = MagicMock()

        config = Configuration(cache_expiration, lambda: gamesave_id)

        cut = GameSave(db, kv, config)
        (result, status) = cut.get(gamesave_id)

        self.assertEqual(result, json.loads(gamesave))
        self.assertEqual(status, 200)
        kv.expire.assert_called_with(gamesave_id, cache_expiration)
        kv.set.assert_called_with(gamesave_id, gamesave)
        db.query.assert_called_with("select gamesave from gamesaves where id='" + gamesave_id + "'")

    def test_retrieving_gamestate_when_not_exists(self):
        gamesave_id = "11111111-2222-1111-2222-000000000000"
        cache_expiration = 999

        db = Object()
        queryresult = Object()
        queryresult.getresult = MagicMock(return_value=[])
        db.query = MagicMock(return_value=queryresult)
       
        kv = Object()
        kv.expire =  MagicMock(return_value=False)

        config = Configuration(cache_expiration, lambda: gamesave_id)

        cut = GameSave(db, kv, config)
        (result, status) = cut.get(gamesave_id)
        self.assertEqual(result, None)
        self.assertEqual(status, 404)
        kv.expire.assert_called_with(gamesave_id, cache_expiration)
        db.query.assert_called_with("select gamesave from gamesaves where id='" + gamesave_id + "'")

class GameSaveListResourceTest(unittest.TestCase):
    def test_creating_new_gamestate(self):
        gamesave_id = "11111111-2222-1111-2222-000000000000"
        gamesave = '{ "hp": 100, "mp": 30 }'
        cache_expiration = 999

        db = Object()
        db.query = MagicMock()
        
        kv = Object()
        kv.set = MagicMock()
        kv.expire =  MagicMock()

        parser = Object()
        parser.parse_args = MagicMock(return_value={ 'gamesave': gamesave })

        config = Configuration(cache_expiration, lambda: gamesave_id)

        cut = GameSaveList(db, kv, parser, config)
        (returned_id, status) = cut.post()

        self.assertEqual(returned_id, gamesave_id)
        self.assertEqual(status, 201)
        kv.set.assert_called_with(gamesave_id, gamesave)
        kv.expire.assert_called_with(gamesave_id, cache_expiration)
        db.query.assert_called_with("insert into gamesaves values ('" + gamesave_id + "', '" + gamesave + "')")
        parser.parse_args.assert_called_once()

if __name__ == '__main__':
    unittest.main()