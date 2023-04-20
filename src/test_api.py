#!/usr/bin/env python3

import unittest
import requests
import json

URL = "http://127.0.0.1:8000"

def isUUID4(maybe_uuid: str) -> bool:
    """
    Validate a string is a UUID V4
    """
    import uuid
    try:
        uuid.UUID(maybe_uuid, version=4)
        return True
    except ValueError:
        return False


class APITester(unittest.TestCase):
    def start_game(self):
        request_data = {
            "num_of_human_player": 4,
            "num_of_ai_player": 4,
            "color_of_player": ["red", "green", "blue", "purple"],
            "board_size": 3
        }
        req = requests.post(URL + "/start_game", data=json.dumps(request_data))
        return req.json()

    def backdoor(self, payload: str):
        """
        Backdoor to game server so I can access information about the game
        that's otherwise inaccessable. please use responsibly
        """
        from requests.utils import quote

        requests.get(URL + "/backdoor", params={"cmd": payload})

    def test_start_game(self):
        res = self.start_game()
        self.assertTrue(isUUID4(res["game_id"]))
        self.assertIsNotNone(res["board_state"])
        self.assertEqual(res["board_state"]["size"], 3)

    def test_sanity(self):
        req = requests.get(URL + "/")
        self.assertEqual(req.json(), {"sanity": "verified"},
                         "Make sure the API is running if this test is failing")

    def test_end_turn(self):
        res = self.start_game()
        gid = res["game_id"]
        params = {
            "game_id": gid,
            "player_colour": "red"
        }
        req = requests.get(URL + "/end_turn", params=params)
        self.assertEqual(req.json(), {"status": "OK"})
#
#
#
    def test_get_player_resources(self):
        res = self.start_game()
        gid = res["game_id"]

        params = {
            "game_id": gid,
            "player_colour": "red"
        }
        req = requests.get(URL + "/player_resources", params=params)
        self.assertEqual(req.json(), {})
        req2 = requests.get(URL + "/updated_player_resources", params=params)
        self.assertNotEqual(req2.json(), {})


    def test_get_available_actions(self):
        res = self.start_game()
        gid = res["game_id"]
        params = {
            "game_id": gid,
            "player_colour": "red"
        }
        req = requests.get(URL + "/available_actions", params=params)
        self.assertTrue("End turn" in req.json())

    def test_buy_dev_card(self):
        gid = self.start_game()["game_id"]
        payload = f"from resources import *; games['{gid}'].players[0] = Resources({{ResourceKind.ore:1,ResourceKind.wool:1,ResourceKind.grain:1}});"
        self.backdoor(payload)
        req = requests.get(URL + "/buy_dev_card", data={"game_id": gid, "player_colour": "red"})
        print(req.json())
        self.assertTrue("card" in req.json().keys())


if __name__ == "__main__":
    unittest.main()
