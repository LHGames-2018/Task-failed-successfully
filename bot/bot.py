from helper import *


class Bot:
    def __init__(self):
        pass

    def before_turn(self, playerInfo):
        """
        Gets called before ExecuteTurn. This is where you get your bot's state.
            :param playerInfo: Your bot's current state.
        """
        self.PlayerInfo = playerInfo


        if self.state != "farm" and self.state != "home":
            self.state = "move"

        #if self.PlayerInfo.CarriedResources < self.PlayerInfo.CarryingCapacity:
        #    self.state = "farm"
        #else:
        #    self.state = "home"

    def execute_turn(self, gameMap, visiblePlayers):
        """
        This is where you decide what action to take.
            :param gameMap: The gamemap.
            :param visiblePlayers:  The list of visible players.
        """

        # Write your bot here. Use functions from aiHelper to instantiate your actions.

        if self.state == "move":
            self.state = "farm"
            return create_move_action(Point(0, -1))

        if self.state == "farm":
            if self.PlayerInfo.CarriedResources < self.PlayerInfo.CarryingCapacity:
                return create_collect_action(Point(-1, 0))
            else:
                self.state = "home"

        if self.state == "home":
            return create_empty_action()

        return create_empty_action()

    def after_turn(self):
        """
        Gets called after executeTurn
        """
        pass
