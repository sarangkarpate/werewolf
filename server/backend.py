import random
from typing import Dict, List


class Role:
    def __init__(self, name: str, party: str):
        self.name = name
        self.party = party

    def __eq__(self, o: object) -> bool:
        if not isinstance(o, Role):
            return False
        return self.name == o.name and self.party == o.party

    def __hash__(self) -> int:
        return hash((self.name, self.party))


class Room():
    def __init__(self, moderator: int):
        self.roles = {}
        self.players = set()
        self.moderator = moderator
        self.started = False

    def add_player(self, user: int):
        if user != self.moderator:
            self.players.add(user)

    def add_players(self, users: List[int]):
        for user in users:
            self.add_player(user)

    def add_role(self, role: Role, count: int = 1):
        if role in self.roles:
            self.roles[role] += count
        else:
            self.roles[role] = count

    def remove_player(self, user: int):
        self.players.discard(user)

    def remove_players(self, users: List[int]):
        for user in users:
            self.remove_player(user)

    # -1 count means to remove all roles
    def remove_role(self, role: Role, count: int = -1):
        if count == -1:
            self.roles.pop(role)
        if role in self.roles:
            self.roles[role] = self.roles[role] - count
            if self.roles[role] < 0:
                self.roles.pop(role)

    def start_game(self) -> Dict[int, Role]:
        roles = []
        for role, count in self.roles.items():
            roles.extend([role] * count)

        players = list(self.players)
        if len(roles) != len(self.players):
            raise Exception("Cannot start game because Role count is {} and Player count is {}".format(len(roles),
                                                                                                       len(self.players)))
        random.shuffle(roles)

        assigned_roles = {}
        for i, player in enumerate(players):
            assigned_roles[player] = roles[i]

        return assigned_roles

    def get_roles(self) -> Dict[Role, int]:
        """
        Returns a mapping of Role to the ID of the player
        :return: Dict
        """
        return self.roles
