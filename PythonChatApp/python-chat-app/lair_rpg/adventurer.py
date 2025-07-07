from lair_rpg.character import Character


class Adventurer(Character):
    def __init__(self, base_health, base_attack) -> None:
        super().__init__(base_health, base_attack)
        self.name = self.generate_name()

    def generate_name(self):
        return ""