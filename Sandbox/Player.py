from Board import *
from Resources import Resources


class Player:

    def __init__(player, color):

        player.color = color

        player.available_settlements = [Settlement(player) for i in range(5)]
        player.available_cities = [City(player) for i in range(4)]
        # TODO: change this so the location of possible roads is accurate
        player.available_roads = [Road(0, player) for i in range(15)]

        player.built_settlements = []
        player.built_cities = []
        player.built_roads = []

        # Victory point related
        player.road_length = 0
        player.knights_played = 0
        player.victory_points = 0
        player.hidden_victory_points = 0

        player.resources = Resources()
        player.development_cards = [] # list of card object?
        player.exchange_rate = {
            # player side to bank: identical resource to 1 target resource
            "brick" : {
                "lumber" : 4,
                "ore" : 4,
                "grain" : 4,
                "wool" : 4
            }, 
            "lumber" :{
                "brick" : 4,
                "ore" : 4,
                "grain" : 4,
                "wool" : 4
            },
            "ore" :{
                "brick" : 4,
                "lumber" : 4,
                "grain" : 4,
                "wool" : 4
            },
            "grain" :{
                "brick" : 4,
                "ore" : 4,
                "lumber" : 4,
                "wool" : 4
            },
            "wool" :{
                "brick" : 4,
                "ore" : 4,
                "grain" : 4,
                "lumber" : 4
            }
            # how to handle the harbour
                # 1. 3:1 harbour: update all 3
                # 2. 2:1 harbour: update like ore in each to 2
        }


    #def builds_settlement(player, location):
    #  player.game.board.add_settlement(location, player)

    #def builds_road(player, location):
    #  player.game.board.add_road(location, player)

    def view_possible_actions():
        # should return list of devcard
        # ask gamemaster
        return []
    

    def builds_settlement(player, location):

        if player.available_settlements:
            settlement = player.available_settlements.pop()
        else:
            raise Exception("Player has no available settlements to build")

        try:
            player.game.add_settlement(location, settlement)
            player.built_settlements.append(settlement)
        except Exception as e:
            player.available_settlements.append(settlement)
            raise e

    def upgrade_settlement(player, location):
        
        if player.available_cities:
            city = player.available_cities.pop()
        else:
            raise Exception("Player has no available cities to build")

        try:
            player.game.upgrade_settlement(location, city)
            player.built_cities.append(city)
        except Exception as e:
            player.available_settlements.append(city)
            raise e
        

    def builds_road(player, location):

        # shall these handel by gamemaster to look over to it
        # when gamemaster give options for player to choose
        if player.available_roads:
            road = player.available_roads.pop()
        else:
            raise Exception("Player has no available roads to build")

        try:
            player.game.add_road(location, road)
            player.built_roads.append(road)
        except Exception as e:
            player.available_roads.append(road)
            raise e

    def request_trade(player, offering: dict, recieving: dict, to_players: str = None ,bank: str = None):
        # check resource
        for offering_resource, quantity in offering.items():
            print("")

        player.game.request()
        

    def play_knight(player, location):
        # check dev care
        

        # should direcly call board to play knight
        pass

    def ends_turn(player):
        player.game.end_turn()
