from helper import *
from random import * 

class Bot:
    def __init__(self):
        self.state = "init"
        self.direction = Point(0,0)
        self.compteur = 0
        pass

    def before_turn(self, playerInfo):
        """
        Gets called before ExecuteTurn. This is where you get your bot's state.
            :param playerInfo: Your bot's current state.
        """

        if self.state == "init":
            self.state = "searchRessource"
        elif self.state == "searchRessource":
            self.state = "walkRessource"
        
        self.PlayerInfo = playerInfo

    def execute_turn(self, gameMap, visiblePlayers):
        """
        This is where you decide what action to take.
            :param gameMap: The gamemap.
            :param visiblePlayers:  The list of visible players.
        """
        if (self.state == "bloquer"):
            if self.compteur > 10:
                self.state = "marcher"
            self.compteur+=1
            random = randint(0, 3)
            if random == 0:
                return create_move_action(Point(1, 0))
            elif  random == 1:
                return create_move_action(Point(0, 1))
            elif random == 2:
                return create_move_action(Point(0, -1))
            else:
                return create_move_action(Point(-1, 0))
        self.compteur = 0
        positions = self.findResource(gameMap)
        positions = self.convertGlobalMapToLocalMap(positions)

        positionObstacle = Point(0,0)
        valider = 0
        # Write your bot here. Use functions from aiHelper to instantiate your actions.
        if (self.PlayerInfo.CarriedResources == self.PlayerInfo.CarryingCapacity):
            valider = 1
            print("on est plein, on veut rentrer")
            if (self.PlayerInfo.HouseLocation.x < self.PlayerInfo.Position.x):
                positionObstacle = Point(self.PlayerInfo.Position.x- 1, self.PlayerInfo.Position.y)
                if gameMap.getTileAt(positionObstacle) != TileContent.Wall and gameMap.getTileAt(positionObstacle) != TileContent.Resource:
                    return create_move_action(Point(-1, 0))
            if (self.PlayerInfo.HouseLocation.x > self.PlayerInfo.Position.x):
                positionObstacle = Point(self.PlayerInfo.Position.x + 1, self.PlayerInfo.Position.y)
                if gameMap.getTileAt(positionObstacle) != TileContent.Wall and gameMap.getTileAt(positionObstacle) != TileContent.Resource:
                    return create_move_action(Point(1, 0))
            if (self.PlayerInfo.HouseLocation.y < self.PlayerInfo.Position.y):
                positionObstacle = Point(self.PlayerInfo.Position.x, self.PlayerInfo.Position.y - 1)
                if gameMap.getTileAt(positionObstacle) != TileContent.Wall and gameMap.getTileAt(positionObstacle) != TileContent.Resource:
                    return create_move_action(Point(0, -1))
            if (self.PlayerInfo.HouseLocation.y > self.PlayerInfo.Position.y):
                positionObstacle = Point(self.PlayerInfo.Position.x, self.PlayerInfo.Position.y + 1)
                if gameMap.getTileAt(positionObstacle) != TileContent.Wall and gameMap.getTileAt(positionObstacle) != TileContent.Resource:
                    return create_move_action(Point(0, 1))
        elif ((abs(positions[0].x - 10) <= 1 and positions[0].y == 10) or (abs(positions[0].y - 10) <= 1 and positions[0].x == 10)):
            print("je me dirige vers une ressource")
            if positions[0].y < 10:
                self.direction = Point(0, -1)
                return create_collect_action(self.direction)
            if positions[0].y > 10:
                self.direction = Point(0, 1)
                return create_collect_action(self.direction)
            if positions[0].x < 10:
                self.direction = Point(-1, 0)
                return create_collect_action(self.direction)
            if positions[0].x > 10:
                self.direction = Point(1, 0)
                return create_collect_action(self.direction)
        print("je me deplace juste")
        if (valider == 1):
            self.state = "bloquer"
        if (positions[0].x < 10):
            self.direction = Point(-1, 0)
            positionObstacle = Point(self.PlayerInfo.Position.x- 1, self.PlayerInfo.Position.y)
            if gameMap.getTileAt(positionObstacle) != TileContent.Wall:
                return create_move_action(self.direction)
            return create_attack_action(self.direction)
        if (positions[0].x > 10):
            self.direction = Point(1, 0)
            positionObstacle = Point(self.PlayerInfo.Position.x + 1, self.PlayerInfo.Position.y)
            if gameMap.getTileAt(positionObstacle ) != TileContent.Wall : 
                return create_move_action(self.direction)
            return create_attack_action(self.direction)
        if (positions[0].y < 10):
            self.direction = Point(0, -1)
            positionObstacle = Point(self.PlayerInfo.Position.y- 1, self.PlayerInfo.Position.y)
            if gameMap.getTileAt(positionObstacle) != TileContent.Wall:
                return create_move_action(self.direction)
            return create_attack_action(self.direction)
        if (positions[0].y > 10):
            self.direction = Point(0, 1)
            positionObstacle = Point(self.PlayerInfo.Position.y + 1, self.PlayerInfo.Position.y)
            if gameMap.getTileAt(positionObstacle) != TileContent.Wall:
                return create_move_action(self.direction)
            return create_attack_action(self.direction)

        return create_collect_action(self.direction)

    def after_turn(self):
        """
        Gets called after executeTurn
        """
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
            distances.append(Point.Distance(self.PlayerInfo.HouseLocation, points[x]))
        while len(distances) > 0:
            index = distances.index(min(distances))
            results.append(points[index])
            points.remove(points[index])
            distances.remove(distances[index])
        return results
    
    def arrayGameMap(self, gameMap):
        results = []
        line = []
        for x in range(0, len(gameMap.tiles)):
            for y in range(0, len((gameMap.tiles[0]))): 
                position = Point(self.PlayerInfo.Position.x + x, self.PlayerInfo.Position.y + y)
                if gameMap.getTileAt(position) == TileContent.Wall or gameMap.getTileAt(position) == TileContent.Resource:
                    line.append("1")
                else:
                    line.append("0")
            results.append(line)
            line = []
        return results

    def convertGlobalMapToLocalMap(self, points):
        for i in range (0, len(points)):
            points[i].x -= (self.PlayerInfo.Position.x - 10)
            points[i].y -= (self.PlayerInfo.Position.y - 10)
        return points