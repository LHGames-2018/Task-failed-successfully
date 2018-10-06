from helper import *
from bot.astar import *
import copy

from helper import *


class Bot:
    def __init__(self):
        self.minerai = Point(0, 0)
        self.next_move = Point(0, 0)
        self.state = "seek"
        self.moves = []
        print("Init called !")
        pass

    def before_turn(self, playerInfo):
        """
        Gets called before ExecuteTurn. This is where you get your bot's state.
            :param playerInfo: Your bot's current state.
        """

        self.PlayerInfo = playerInfo
        print("position joueur: ")
        print(self.PlayerInfo.Position)

    def execute_turn(self, gameMap, visiblePlayers):
        """
        This is where you decide what action to take.
            :param gameMap: The gamemap.
            :param visiblePlayers:  The list of visible players.
        """

        print("Current state: " + str(self.state))

        if self.state == "seek":
            positions = self.findResource(gameMap)
            if positions.__len__() == 0:
                self.state = "go_back_home"
            else:
                self.minerai = copy.deepcopy(positions[0])
                for x in range(len(positions)):
                    print("avant x : ")
                    print(positions[x].x)
                    print("avant y : ")
                    print(positions[x].y)
                position = self.convertGlobalMapToLocalMap(positions)
                print("position ressource")
                for x in range(len(positions)):
                    print("apres x : ")
                    print(positions[x].x)
                    print("apres y : ")
                    print(positions[x].y)
                map = self.arrayGameMap(gameMap)
                print("map")
                print(map)

                bot_start = (10, 10)
                bot_end = (positions[0].x, positions[0].y)

                path = astar(map, bot_start, bot_end)

                if path == None:
                    self.state = "go_back_home"
                else:
                    self.moves = convertMove(path)
                    self.state = "endseek"

        elif self.state == "move_to_farm":
            if self.moves.__len__() > 0:
                self.next_move = self.moves[0]
                self.moves.pop(0)
                return create_move_action(self.next_move)
            else:
                print("Last move : ", self.next_move)
                self.state = "end_move_to_farm"
                return create_collect_action(self.next_move)

        elif self.state == "farm":
            if self.PlayerInfo.CarryingCapacity == self.PlayerInfo.CarriedResources:
                self.state = "endfarm"
            elif gameMap.getTileAt(self.minerai) != TileContent.Resource:
                self.state = "seek"
            else:
                return create_collect_action(self.next_move)

        elif self.state == "go_back_home":
            map = self.arrayGameMap(gameMap)
            print("map")
            print(map)

            bot_start = (10, 10)

            house_x = abs((self.PlayerInfo.Position.x - 10) - self.PlayerInfo.HouseLocation.x)
            house_y = abs((self.PlayerInfo.Position.y - 10) - self.PlayerInfo.HouseLocation.y)

            bot_end = (house_x, house_y)

            path = astar(map, bot_start, bot_end)

            print(path)

            self.moves = convertMove(path)

            self.state = "move_to_home"

        elif self.state == "move_to_home":
            if self.moves.__len__() > 0:
                self.next_move = self.moves[0]
                self.moves.pop(0)
                return create_move_action(self.next_move)
            else:
                self.state = "home"
                print("House : ", self.PlayerInfo.HouseLocation)
                print("Player : ", self.PlayerInfo.Position)
                return create_empty_action()

        elif self.state == "try_upgrade":
            self.state = "end_upgrade"
            return create_upgrade_action(UpgradeType.CollectingSpeed)

        print(gameMap)
        return create_empty_action()

    def after_turn(self):
        """
        Gets called after executeTurn
        """
        if self.state == "endseek":
            self.state = "move_to_farm"
        elif self.state == "end_move_to_farm":
            self.state = "farm"
        elif self.state == "endfarm":
            self.state = "go_back_home"
        elif self.state == "home":
            self.state = "try_upgrade"
        elif self.state == "end_upgrade":
            self.state = "seek"
        pass

    def findResource(self, gameMap):
        results = []
        for x in range(self.PlayerInfo.Position.x - 10, self.PlayerInfo.Position.x + 10):
            for y in range(self.PlayerInfo.Position.y - 10, self.PlayerInfo.Position.y + 10):
                position = Point(x, y)
                if gameMap.getTileAt(position) == TileContent.Resource:
                    results.append(position)
        return self.bestPoint(results)

    def bestPoint(self, points):
        results = []
        distances = []
        for x in range(len(points)):
            distances.append(Point.Distance(self.PlayerInfo.Position, points[x]))
        while len(distances) > 0:
            index = distances.index(min(distances))
            results.append(points[index])
            points.remove(points[index])
            distances.remove(distances[index])
        return results

    def arrayGameMap(self, gameMap):
        results = []
        line = []
        for y in range(0, len(gameMap.tiles)):
            for x in range(0, len((gameMap.tiles[0]))):
                origine_x = self.PlayerInfo.Position.x - 10
                origine_y = self.PlayerInfo.Position.y - 10

                position = Point(origine_x + x, origine_y + y)
                if gameMap.getTileAt(position) == TileContent.Wall or gameMap.getTileAt(
                        position) == TileContent.Resource:
                    line.append(1)
                else:
                    line.append(0)
            results.append(line)
            line = []
        return results

    def convertGlobalMapToLocalMap(self, points):
        for i in range(0, len(points)):
            points[i].x -= (self.PlayerInfo.Position.x - 10)
            points[i].y -= (self.PlayerInfo.Position.y - 10)
        return points
