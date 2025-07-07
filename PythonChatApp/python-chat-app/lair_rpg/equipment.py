from random import randint

class Equipment():
    def __init__(self, slot) -> None:
        self.slot = type
        
        self.health_boost = randint(0, 999)
        self.damage_boost = randint(0, 999)
        self.value = self.health_boost + self.damage_boost

        self.name = self.set_name()

    def set_name(self):
        pass
        #TODO generate random names based on nouns and verbs
        #Higher value = longer name
        #object noun based on slot
        # "[]'s [] [slot] of the [] []", etc
        # Bastard's Bastard Sword of the Bastard Bastard

