from lair_rpg.character import Character

class Monster(Character):
    def __init__(self, base_health, base_attack) -> None:
        super().__init__(base_health, base_attack)
        
        self.hoard = []

    def equip(self, equipment_index):

        equipment_item = self.hoard[equipment_index]
        slot = equipment_item.slot

        self.hoard.append(self.equipment[slot])
        self.equipment[slot] = self.hoard.pop(equipment_item)

        self.get_equiped_stats()

    def get_hoard_value(self):
        return sum([item.value for item in self.hoard])
