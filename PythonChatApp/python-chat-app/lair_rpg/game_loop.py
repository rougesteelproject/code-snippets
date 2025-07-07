import socket
import threading

from random import randint
from client import Client
from lair_rpg.adventurer import Adventurer
from lair_rpg.monster import Monster

class LairRpg(Client):
    def __init__(self, server, port, player_client) -> None:
        
        self.FORMAT = 'utf-8'

        self.DISCONNECT_MESSAGE = "!disconnect"
        #If users do not propperly disconnect by sending this message, the server may keep their connection ope, then they can't reconnect
        self.SET_NICKNAME_MESSAGE = "!nick"

        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        #SOCK_STREAM is TCP
        self.sock.connect((server, port))

        self.nickname = 'lair_rpg'

        self.gui_done = False
        self._running = True

        gui_thread = threading.Thread(target=self.gui_loop)
        recieve_thread = threading.Thread(target=self.recieve)

        gui_thread.start()
        recieve_thread.start()

        self.player_client = player_client
        self.monster = None
        self.adventurers = []
        self.unit_list = []
        self.round_count = 0

    def get_input(self, prompt):
        #TODO return self.server.get_input(self.client, prompt)

    def send_message(self, message):
        #TODO direct_message(self.client, message)

    def run_game(self):

        self.make_monster()

        self.run_wave()


    def make_monster(self):
        self.monster = Monster(5, 5)
        self.unit_list.append(self.monster)

    def make_adventurers(self):
        #Add adventurers to list until the sum of the values of their equipment is more than the monster's sum
        combat_level = self.monster.get_equipment_sum()
        while sum([adventurer.get_equipment_sum() for adventurer in self.adventurers]) < combat_level:
            base_health = randint(1, 9)
            min_attack = 10 - base_health
            self.adventurers.append(Adventurer(base_health, min_attack))

        #Remove last adventurer
        if len(self.adventurers) > 1:
            list.pop(-1)

    def player_attack(self):
        #On monster (player) turn, ask who to attack
        attack_prompt = f'Choose a pesky invader to attack:\n'
        for index, unit in enumerate(self.unit_list):
            if unit != self.monster and unit.get_is_dead == False:
                attack_prompt += f'{index}: {unit.name} \n'

        target_index = self.get_input(attack_prompt)

        unit = self.unit_list[target_index]

        if unit.get_is_dead():
            self.send_message(f'You attack the {unit.name}, who was already dead!')
        else:
            self.send_message(f'You attack the {unit.name}')
            self.unit.take_damage(self.monster.current_attack)
            #When an adventurer is dead, add their loot to the hoard, sending the names one-by-one to the player
            if unit.get_is_dead():
                self.monster.hoard.extend([item for item in unit.equipment.values()])


    def run_round(self):
        for unit in self.unit_list:
            if unit.get_is_dead() == False:
                if unit == self.monster:
                    #On monster (player) turn, ask who to attack
                    self.player_attack()
                    
                else:
                    self.send_message(f'{unit.name} attacks you for {unit.current_attack}!')
                    self.monster.take_damage(unit.current_attack)
                    self.send_message(f'Your health is now {self.monster.current_health}!')
                    if self.monster.get_is_dead():
                        self.send_message('You are dead!')
                        break

        self.round_count += 1

        self.unit_list = [unit for unit in self.unit_list if unit.get_is_dead() == False]

    def player_death(self):
        self.send_message(f'You have died. You survived for {self.round_count} rounds. You amassed a trasure hoard worth {self.monster.get_hoard_value()}.')
        player_input = self.get_input("Do you wish to play again? Press y to play, or any key to quit. \n")

        if player_input == 'y':
            self.run_game()
        else:
            self.stop()

    #While a "client", the game runs itself/ is a thread of the server

    #TODO a DM system, "!DM [nickname]", then clinet appends "!DM [nickname]" to the message until "!DM [nickname] !EndDM
    #TODO use dms to run the game
    #TODO game_loop overwrite the client listener to handle responses "!TAG {response}" to different prompts
    #The client responds to "!PROMPT !TAG {propmpt}" with "!TAG {response}"
    #TODO change player_input to a class property
    #TODO when a player responds with "!TAG {response}, run the corresponding 'loop' just once"

    def player_equipment_round(self):
        player_input = 'y'
        while player_input == 'y':

            self.send_message("You have the following items in your hoard:\n")
            for index, item in enumerate(self.monster.hoard):
                self.send_message(f'{index}: {item.name}\n')

            player_input = self.get_input('Do you want to equip any more items?\n')

        

    def run_wave(self):
        self.make_adventurers()

        #TODO randomize self.unit_list

        while len(self.unit_list) > 1:
            self.run_round()

        if self.monster.get_is_dead():
            self.player_death()
        else:
            self.player_equipment_round()