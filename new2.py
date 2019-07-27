from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.floatlayout import Layout
from kivy.uix.image import Image
import random
from kivy.graphics import *
from kivy.animation import Animation
from kivy.core.window import Window
Window.fullscreen = 'auto'
from kivy.clock import Clock
from functools import partial
import copy
class Card(Image):#obect of card for list cards of the game
    def __init__(self,number,shape,flag_quzar,source,Board):#Build a card that consist of shape,number ,is he quzar,source of image ,score for the Ai and 2 values that will deide when to be dragged
        super(Card, self).__init__()
        self.shape = shape
        self.number = number
        self.flag_quzar = flag_quzar
        self.source = source
        self.Board = Board
        self.to_move = False#State if you can start move the card
        self.can_be_dragged = True#State if you can start drag the card
        self.score=0
    def on_touch_down(self,touch):  # Check if there is a card with his shape in the battle and check on_place conditions and then u can move him
        if self.collide_point(touch.x, touch.y) and self.can_be_dragged == True:
            self.to_move = True
    def on_touch_move(self, touch):  # Update position by x and y ebery move of the card(input mouse)
        if self.to_move:
            self.x = touch.x - self.width / 2
            self.y = touch.y - self.height / 2
    def on_touch_up(self, touch):  # Unable to move when realesed, if the conditions are good and you can put the card put him on list battle
        self.to_move = False
        if self.on_place() != False :
            self.can_be_dragged = False
    def on_place(self):  # Check if the card in batlle position and if he even can return place that can be put
        for i in range(6):
            if (self.Board.pos_rectangle_list[i][0] < self.x < self.Board.pos_rectangle_list[i][0] + 180 and
                            self.Board.pos_rectangle_list[i][1] < self.y < self.Board.pos_rectangle_list[i][1] + 180):
                if (len(self.Board.cards_battle[i]) == 0 and self.Board.turn_attack==0 and self.can_be_on_board()):
                    self.Board.remove_card(self)
                    self.Board.remove_from_unkown(self)
                    self.can_be_dragged = False
                    self.Board.cards_battle[i].append(self)
                    del self.Board.list_players[0][self.find_card()]
                    self.x = self.Board.pos_rectangle_list[i][0] + 40
                    self.y = self.Board.pos_rectangle_list[i][1]
                    self.Board.stuck_the_other()
                    self.Board.organize_the_cards(0)
                    return i
                elif len(self.Board.cards_battle[i]) == 1 and self.check_bigger( self.Board.cards_battle[i][0])==True:
                    self.Board.remove_card(self)
                    self.Board.remove_from_unkown(self)
                    self.can_be_dragged = False
                    self.Board.cards_battle[i].append(self)
                    del self.Board.list_players[0][self.find_card()]
                    self.x = self.Board.pos_rectangle_list[i][0] + 40
                    self.y = self.Board.pos_rectangle_list[i][1] + 30
                    self.Board.organize_the_cards(0)
                    return i
        return False
    def find_card(self):  # find which card was placed return which card it is
        for i in range(len(self.Board.list_players[0])):
            if (self.number == self.Board.list_players[0][i].number and self.shape == self.Board.list_players[0][
                i].shape):
                return i
    def check_bigger(self, card):  # function check if the cardscan beat(answer) the other return true if it can false for any other option
        if (card.flag_quzar == False and self.flag_quzar==False):
            if (self.shape == card.shape and self.number > card.number):
                return True
            else:
                return False
        elif(card.flag_quzar == False and self.flag_quzar==True):
            return True
        elif(self.flag_quzar == True and card.flag_quzar==True):
                if (self.number > card.number):
                    return True
                else:
                    return False
    def create_card(self):#Return a card but without graffics with same values
        return reg_card(self.number,self.shape,self.flag_quzar,self.score)
    def can_be_on_board(self):#Check if the card we attacked with is good for attacking return true if it can ele false
        counter=0
        for i in self.Board.cards_battle:
            for j in i:
                if j.number==self.number:
                    return True
                counter+=1
        if counter==0:
            return True
        return False
class reg_card():#Card but without graffics
    def __init__(self, number, shape, flag_quzar,score):
        self.shape = shape
        self.number = number
        self.flag_quzar = flag_quzar
        self.score=score

    def check_bigger(self, card):  # function of card without graffic check if the cardscan beat(answer) the other return true if it can false for any other option
        if (card.flag_quzar == False and self.flag_quzar == False):
            if (self.shape == card.shape and self.number > card.number):
                return True
            else:
                return False
        elif (card.flag_quzar == False and self.flag_quzar == True):
            return True
        elif (self.flag_quzar == True and card.flag_quzar == True):
            if (self.number > card.number):
                return True
            else:
                return False
class board_for_AI():#Board of the game but without graffics
    def __init__(self,):#Build empty list that will consist the battle
        self.battle_list=[[] for i in xrange(6)]
        self.list_of_players=[[] for i in xrange(2)]
    def find_empty_place2(self):#For the attck find empty place other return False
        for i in range(6):
            if len(self.battle_list[i])==0:
                return i
        return False
    def find_need_defence(self):#Find in the list battle
        for i in range(6):
            if len(self.battle_list[i])==1:
                return i
        return False
    def list_battle_attack2(self):#Return the list of all attacks that
        list_battle = []
        for i in range(6):
            if len(self.battle_list[i]) == 1:
                list_battle.append(self.battle_list[i][0])
            elif len(self.battle_list[i]) == 2:
                list_battle.append(self.battle_list[i][0])
                list_battle.append(self.battle_list[i][1])
        return list_battle
    def is_full(self):#Check if there were six attack and there is no place for more attacks return true if board is full else, false
        for i in range(6):
            if len(self.battle_list[i])==0:
                return False
        return True

    def is_empty(
            self):  # Check if there were six attack and there is no place for more attacks return true if board is full else, false
        for i in range(6):
            if len(self.battle_list[i]) != 0:
                return False
        return True
    def take_cards_from_board(self,player):#When player can not counter the attack he will take alll card that on board
        for i in range(6):
            for j in self.battle_list[i]:
                self.list_of_players[player].append(j)
        self.battle_list=[[] for j in xrange(6)]
# class that contains all the data structures of the game
class Board(Layout):
    # Builds the board
    def __init__(self, **kwargs):#Function that build the board of the game. The board consist of the whole data base of the game and the graffic o the game
        super(Board, self).__init__(**kwargs)
        self.blank1 = "blank1.jpg"
        self.turn_attack = 0  # Check who is attacking now
        self.turn_deffedned = 1  # check who is deffend now
        self.sources = ['leaf6.jpg', 'heart6.jpg',
                        'dimond6.jpg', 'tiltan6.jpg', 'leaf7.jpg', 'heart7.jpg', 'dimond7.jpg', 'tiltan7.jpg',
                        'leaf8.jpg', 'heart8.jpg',
                        'dimond8.jpg', 'tiltan8.jpg', 'leaf9.jpg', 'heart9.jpg', 'dimond9.jpg', 'tiltan9.jpg',
                        'leaf10.jpg', 'heart10.jpg',
                        'dimond10.jpg', 'tiltan10.jpg', 'leafJ.jpg', 'heartJ.jpg', 'dimondJ.jpg', 'tiltanJ.jpg',
                        'leafQ.jpg', 'heartQ.jpg',
                        'dimondQ.jpg', 'tiltanQ.jpg', 'leafK.jpg', 'heartK.jpg', 'dimondK.jpg', 'tiltanK.jpg',
                        'leafA.jpg'
            ,   'heartA.jpg', 'dimondA.jpg', 'tiltanA.jpg']

        self.list_cards = []
        self.pos_rectangle_list = list()  # Position of the battle's rektangles
        self.cards_battle = [[], [], [], [], [], []]  # 2 D list that keep the card of the current battle
        self.list_players = [[], []]  # 2D list that contain list of cards for every player
        self.computer_pos_card = []
        self.list_exist_cards = []
        self.list_known = []
        self.start_button = Button(font_size=14, pos=(800, 800), height=150,
                                   width=400,background_normal ='image.jpg',text_color=(0,0,0,1) )
        self.add_widget(self.start_button)
        self.start_button.bind(on_press=self.start)
        self.add_widget(Image(source='instr.png',pos=(700,0),height=1000,
                                   width=1000))
    def creat_list_cards(self):#Function that get list ad build in this list the cards of the game
        shapes = ['leaf', 'heart', 'diamond', 'clubs']
        num = 0
        for i in range(6, 15):#15
            for j in shapes:
                self.list_cards.append(Card(i, j, False, self.sources[num],self,))
                num += 1

    def restart_game(self): # function that restart the original board's class
        self.canvas.clear()
        self.clear_widgets()
        self.__init__()


    def start_game(self):#Function that updates the data of the structures and initializes the graphics
        self.cheat = Button(text='cheat turn', font_size=14, pos=(1400, 200), height=100,
                            width=100)
        self.cheat_flag = False
        self.passed = Button(text='Pass turn', font_size=14, pos=(1200, 200), height=100,
                             width=100)  # Button that when is pressed it is mean the player end his turn
        self.cheat.bind(on_press=self.cheated)
        self.grabbed = Button(text='grab', font_size=14, pos=(1200, 315), height=100,
                              width=100)  # Button that when is pressed it is mean the player i grabbed the card
        self.passed.bind(on_press=self.pass_turn)
        self.grabbed.bind(on_press=self.grabbed_2)
        self.add_widget(self.grabbed)
        self.add_widget(self.passed)
        self.add_widget(self.cheat)
        self.creat_list_cards()
        self.scores()
        self.change_size_of_cards()
        self.buttonrest = Button(text="restart", pos=(100, 500))
        self.buttonrest.bind(on_press=lambda x:self.restart_game())
        self.add_widget(self.buttonrest)
        random.shuffle(self.list_cards)
        for i in range(len(self.list_cards)):
            self.list_exist_cards.append(
                reg_card(self.list_cards[i].number, self.list_cards[i].shape, self.list_cards[i].flag_quzar,self.list_cards[i].score))
        self.give_cards()
        self.quzar = self.list_cards.pop()
        self.quzar.flag_quzar = True
        self.quzar.can_be_dragged = False
        self.quzar.x = 1200
        self.quzar.y = 600
        self.list_game = Image(source=self.blank1, x=1200, y=450, width=115, height=115)
        self.add_widget(self.quzar)
        self.list_cards.append(self.quzar)
        self.show_num_cards = Label(text='there are ' + str(len(self.list_cards)) + ' cards', x=1100, y=470)
        self.add_widget(self.show_num_cards)
        self.add_widget(self.list_game)
        self.change_quzar()
        self.prepre_battle()
        self.cards_on_board()
        self.stuck_cards()
        self.lab1 = Label(text='attack' + ' ' + str(self.turn_attack + 1), x=500, y=500)
        self.add_widget(self.lab1)
        self.lab2 = Label(text='def' + ' ' + str(self.turn_deffedned + 1), x=800, y=500)
        self.name_one=Label(text='human player-1',pos=(700,150))
        self.name_two = Label(text='computer player-2', pos=(700, 800))
        self.add_widget(self.name_one)
        self.add_widget(self.name_two)
        self.add_widget(self.lab2)
        self.lets_start_button=Button(text='lets start',pos=(1200,800),on_press=lambda x:self.who_will_start())
        self.add_widget(self.lets_start_button)


    def scores(self):#Functions that determines points to every card
        for i in range(len(self.list_cards)):
            self.list_cards[i].score =self.list_cards[i].number
            if self.list_cards[i].flag_quzar == True:
                self.list_cards[i].score += 9
    def remove_card(self,card): #Function that changes the reminimg list of cards which are not owned by the players.
        # This list at the end of the game will turn to the list of the player (when there is none list of cards to take from)
        for i in range(len(self.list_exist_cards)):
            if card.number==self.list_exist_cards[i].number and card.shape==self.list_exist_cards[i].shape:
                del self.list_exist_cards[i]
                break
    def start(self, v): #Function that transfer the initial screen to the main screen of the game
        self.clear_widgets()
        self.start_game()
    def cheated(self,v): #Function  will be used to check the player cards and to the future movements
        if self.cheat_flag==False:
            for i in range(len(self.computer_pos_card)):
                self.list_players[1][i].pos=self.computer_pos_card[i].pos
                self.remove_widget(self.computer_pos_card[i])
                self.add_widget( self.list_players[1][i])
        else:
            for i in range(len(self.computer_pos_card)):
                self.list_players[1][i].pos = self.computer_pos_card[i].pos
                self.remove_widget(self.list_players[1][i])
                self.add_widget(self.computer_pos_card[i])
        self.cheat_flag=not self.cheat_flag
    def grabbed_2(self, v): #Function that will be called when the button grab will be pressed.
        #This function will be enabled only when the player needs to take cards from the board
        if  self.end_game_check()==False and self.cheat_flag==False:
            if self.turn_deffedned == 0 and type(self.find_not_deffedned()) == int:
                self.take_cards_from_board(0)
                self.turn_attack=1
                self.turn_deffedned=0
                self.lab1.text = 'attack' + ' ' + str(self.turn_attack + 1)
                self.lab2.text = text = 'defenned' + ' ' + str(self.turn_deffedned + 1)
                Clock.schedule_once(partial(self.attack_computer, self.turn_attack), 1.5)
                self.stuck_cards()
                if len(self.list_cards) != 0:
                    self.take_cards_from_list(1)
    def pass_turn(self, v): #Function that will be called when the button pass will be pressed.
        #The function will be called only when a turn is passed to the other player
        if self.end_game_check()==False and self.cheat_flag==False:
            if self.turn_attack == 0:
                if type(self.find_not_deffedned())==int:
                    Clock.schedule_once(partial(self.deffened_computer, 1), 1.5)
                    self.stuck_the_other()
                else:
                    for i in range(6):
                        for j in range(len(self.cards_battle[i])):
                            self.remove_widget(self.cards_battle[i][0])
                            del self.cards_battle[i][0]
                    self.cards_battle=[[] for i in xrange(6) ]
                    self.turn_attack=1
                    self.turn_deffedned=0
                    self.lab1.text = 'attack' + ' ' + str(self.turn_attack + 1)
                    self.lab2.text = text = 'defenned' + ' ' + str(self.turn_deffedned + 1)
                    if len(self.list_cards) != 0:
                        self.take_cards_from_list(0)
                    if len(self.list_cards) != 0:
                        self.take_cards_from_list(1)
                    Clock.schedule_once(partial(self.attack_computer, self.turn_attack), 1.5)
            elif self.turn_deffedned == 0:
                Clock.schedule_once(partial(self.attack_computer, 1), 1.5)
    def remove_from_unkown(self,card): #Function that removes cards, that the computer remembers that the player had, when he put them on board.
        for i in range(len(self.list_known)):
            if card.number == self.list_known[i].number and card.shape == self.list_known[i].shape:
                del self.list_known[i]
                break

    def change_size_of_cards(self): #Function that changes the size of the cards to the correct size
        for i in range(len(self.list_cards)):
            self.list_cards[i].width = 115
            self.list_cards[i].height = 115

    def give_cards(self): #Function that divides cards to each player
        for j in range(6):
            for i in range(len(self.list_players)):
                if i == 1:
                    self.remove_card(self.list_cards[0])
                self.list_players[i].append(self.list_cards[0])
                del self.list_cards[0]
                if (i != 0):
                    self.list_players[i][j].can_be_dragged = False
    def change_quzar(self): # Function that replaces the flag to true for every card that have the same shape as the quzar
        for j in range(6):
            for i in range(len(self.list_players)):
                if (self.list_players[i][j].shape == self.quzar.shape):
                    self.list_players[i][j].flag_quzar = True
        for i in range(len(self.list_cards)):
            if (self.list_cards[i].shape == self.quzar.shape):
                self.list_cards[i].flag_quzar = True

    def prepre_battle(self): #Function that prepares the place where the battle of the game will occur
        x = 400
        y = 580
        for i in range(0, 3):
            self.pos_rectangle_list.append((x, y))
            with self.canvas:
                Color(255 / 255.0, 219 / 255.0, 88 / 255.0)
                Rectangle(size=(190, 190), pos=(x - 5, y - 5))
                Color(0, 0, 0)
                Rectangle(pos=self.pos_rectangle_list[i], size=(180, 180))
            x += 250
        x = 400
        y = 330
        for i in range(3, 6, 1):
            self.pos_rectangle_list.append((x, y))
            with self.canvas:
                Color(255 / 255.0, 219 / 255.0, 88 / 255.0)
                Rectangle(size=(190, 190), pos=(x - 5, y - 5))
                Color(0, 0, 0)
                Rectangle(pos=self.pos_rectangle_list[i], size=(180, 180))
            x += 250

    def cards_on_board(self): #Function that adds graphically the cards to the layout
        y = 20
        x = 200
        for i in range(6):  # Loop for first player
            self.list_players[0][i].x = x
            self.list_players[0][i].y = y
            self.add_widget(self.list_players[0][i])
            x += 200
        y = 900
        x = 500
        for i in range(6):  # Loop for second player
            card = Image(source=self.blank1, x=x, y=y, width=115, height=115)
            self.add_widget(card)
            self.computer_pos_card.append(card)
            x += 40
    def who_will_start(self): #Function that determines who will start according to which player have bigger quzar
        lowest_card_player = 15
        for i in range(len(self.list_players)):
            for j in range((len(self.list_players[i]))):
                if (self.list_players[i][j].flag_quzar == True and self.list_players[i][
                    j].number < lowest_card_player):
                    if i == 0:
                        self.turn_attack = 0
                        self.turn_deffedned = 1
                        lowest_card_player = self.list_players[i][j].number

                    elif i==1:  
                        self.turn_attack = 1
                        self.turn_deffedned =0
                        lowest_card_player = self.list_players[i][j].number
        if (self.turn_attack == 0):
            self.free_cards()
        else:
            self.stuck_cards()
        self.lab1.text = 'attack' + ' ' + str(self.turn_attack + 1)
        self.lab2.text = text = 'defenned' + ' ' + str(self.turn_deffedned + 1)
        self.attack_computer(self.turn_attack, 1)
        self.remove_widget(self.lets_start_button)
    def stuck_cards(self):  #Function that does'nt let the player to move cards
        for i in range(len(self.list_players[0])):
            self.list_players[0][i].can_be_dragged = False

    def free_cards(self):  #Function that let the player move cards
        for i in range(len(self.list_players[0])):
            self.list_players[0][i].can_be_dragged = True

    def stuck_the_other(self): #Function that let the player move the matching cards
        if self.is_empty() == True:
            self.free_cards()
        else:
            for j in range(len(self.list_players[0])):
                for i in range(len(self.cards_battle)):
                    for k in range(len(self.cards_battle[i])):
                        if (self.list_players[0][j].number == self.cards_battle[i][k].number):
                            self.list_players[0][j].can_be_dragged = True

    def organize_the_cards(self, player): #Function that organizes after every turn
        if player == 0:
            x = 200
            y = 20
            t =105
            for i in range(len(self.list_players[0])):
                self.list_players[0][i].pos = (x, y)
                x += t
        elif player == 1:
            y = 900
            x = 500
            for i in range(len(self.list_players[player])):  # Loop for second player
                self.computer_pos_card[i].pos = (x, y)
                x += 40
    def take_cards_from_list(self,player): #Function that gives to every player number of cards till he has 6 in a turn (till the package of cards ends)
        while (len(self.list_cards) != 0 and len(self.list_players[player]) < 6):
            if len(self.list_cards) == 1:
                self.add_widget(Label(pos=(1200,550),text=self.list_cards[0].shape))
                self.remove_widget(self.list_cards[0])
            if player==1:
                self.remove_card(self.list_cards[0])
            self.list_players[player].append(self.list_cards[0])
            del self.list_cards[0]
            if player == 0:
                k=len(self.list_players[0])-1
                self.remove_widget(self.list_players[player][k])
                self.add_widget(self.list_players[player][k])
            else:
                if len(self.list_players[1])!=0:
                    self.computer_pos_card.append(
                    Image(source=self.blank1, x=20,y=self.computer_pos_card[len(self.computer_pos_card) - 1].y + 40, width=115,
                              height=115))
                else:
                    self.computer_pos_card.append(
                        Image(source=self.blank1, pos=(500,900),
                          width=115,
                          height=115))
                self.add_widget(self.computer_pos_card[len(self.computer_pos_card) - 1])
        self.show_num_cards.text = 'there are ' + str(len(self.list_cards)) + ' cards'
        self.organize_the_cards(player)

    def take_cards_from_board(self, player): #Function that transfers the vards to the player that did not succeed in his turn
        for i in range(len(self.cards_battle)):
            for j in range(len(self.cards_battle[i])):
                if player==0:
                    self.list_known.append(self.cards_battle[i][0])
                self.remove_widget(self.cards_battle[i][0])
                self.list_players[player].append(self.cards_battle[i][0])
                del self.cards_battle[i][0]
                if player == 0:
                    self.add_widget(self.list_players[player][len(self.list_players[0]) - 1])
                else:
                    self.computer_pos_card.append(Image(source=self.blank1, x=20,
                              y=self.computer_pos_card[len(self.computer_pos_card) - 1].y + 40,
                              width=115, height=115))
                    self.add_widget(self.computer_pos_card[len(self.computer_pos_card) - 1])
        self.organize_the_cards(player)
        self.cards_battle = [[], [], [], [], [], []]

    def deffened_computer(self, player, dt): #Function that performs defensive move for the computer
        if player == 0:
            self.free_cards()
            return 0
        t = self.find_not_deffedned()
        while (type(t) == int and self.is_full() == False):
            the_card = self.find_card_to_deffend(self.cards_battle[t][0], player)
            if (type)(the_card) == int:
                self.add_card_to_board(the_card, t, player, False)
                t = self.find_not_deffedned()
            else:
                self.take_cards_from_board(player)
                self.free_cards()
                self.cards_battle = [[], [], [], [], [], []]
                t = False
                if len(self.list_cards) != 0:
                    self.take_cards_from_list(0)



    def find_not_deffedned(self): #Function that seraches in the list of battle a card without defence, returns true if finds else false
        for i in range(6):
            if len(self.cards_battle[i]) == 1:
                return i
        return False

    def find_empty_place(self): #Function that seraches in the list of battle an empty place , returns true if finds else false
        for i in range(6):
            if len(self.cards_battle[i]) == 0:
                return i
        return False
    def how_much_shapes(self,card): #Function that returns score to the player according to how many cards are with same shape
        if card.shape==self.list_cards[-1].shape:
            return 20
        counter=0
        for i in self.list_players[1]:
            if i.shape==card.shape and(card.number!=i.number and card.shape!=i.shape) :
                counter+=1
        if counter==0:
            return 10
        if counter==1:
            return 5
        if counter==2:
            return 0
        return -5
    def will_attack_me(self,card): #Function that searches if the human player has same card as the computer, returns true if finds else false
        for i in self.list_known:
            if i.number==card.number:
                return True
        return False

    def add_card_to_board(self, card_place, rec_place, player,
                          flag):  # Function that gets card place in the list,the number of recatngle,
        # players' number and flag:true for attack false or def and put the card in the battle
        self.remove_widget(self.computer_pos_card[card_place])
        self.list_players[player][card_place].x = self.computer_pos_card[card_place].x
        self.list_players[player][card_place].y = self.computer_pos_card[card_place].y
        del self.computer_pos_card[card_place]
        self.add_widget(self.list_players[player][card_place])
        if flag == True:
            anim = Animation(x=self.pos_rectangle_list[rec_place][0] + 40, y=self.pos_rectangle_list[rec_place][1])
            anim.start(self.list_players[player][card_place])
        else:
            anim = Animation(x=self.pos_rectangle_list[rec_place][0] + 40,
                             y=self.pos_rectangle_list[rec_place][1] + 40)
            anim.start(self.list_players[player][card_place])
        self.cards_battle[rec_place].append(self.list_players[player][card_place])
        del self.list_players[player][card_place]
    def special_condition(self,card):#Function that get a card
        #If it is a quzar and it is the end of the game(less than 5 cards in the pack) return true else false
        if card.flag_quzar==True and self.list_end()!=0:
            return True
        return False
    def find_card_to_deffend(self, card, player): #Function that searches card to protect from attacking card.
        #when there is pack of cards to take from it searches according tactics, when there isn't it searches by brutforce.
        #Returns number of card if it finds it else false.
        if len(self.list_cards)!=0:
            options = []
            for i in range(len(self.list_players[player])):
                if self.list_players[player][i].check_bigger(card):
                    options.append(reg_card(self.list_players[player][i].number, self.list_players[player][i].shape,
                                            self.list_players[player][i].flag_quzar,
                                            self.list_players[player][i].score))
            if len(options) == 0:
                return False
            score_list = []
            for i in options:
                shapes=self.how_much_shapes(i)
                removal=0
                if self.will_attack_me(i)==True:
                    removal=25
                score=100-i.score*2-shapes-removal-self.list_end()
                if score>50:
                    score_list.append((score,i))

            max=0
            for j in range (len(score_list)):
                if max==0:
                    if score_list[j][0] > max and self.special_condition(score_list[j][1])==False :
                        max=score_list[j]
                elif score_list[j][0]>max[0] and self.special_condition(score_list[j][1])==False :
                    max=score_list[j]
            if max==0:
                return False
            elif max[0]>50:
                return self.find_this_card(max[1])
            return False
        else:
            board_for_requrse = board_for_AI()
            self.build_board(board_for_requrse)
            self.create_regu_list_players(board_for_requrse)
            options = self.find_defence_option(1, board_for_requrse)
            print options,'zzzzzzzzzzz'
            need_board_to_win = []
            if options!=None:
                for i in options:
                    if self.recurse_find_card(self.find_attack_option(1, i), 0, True, copy.deepcopy(i)) == True:
                        print 'got one'
                        self.print_board(i.battle_list)
                        need_board_to_win = i
                        break
            print need_board_to_win,'oooooooooooo'
            the_card=''
            if need_board_to_win == []:
                return False

            for i in range(6):
                if len(need_board_to_win.battle_list[i])!=len(self.cards_battle[i]):
                    the_card=i
                    break
            print the_card,'jjjjjjj'
            b=self.find_this_card(need_board_to_win.battle_list[the_card][1])
            return b
    #from here this i the AI
    def build_board(self,board_none_grafic): #Function that builds board of the game without graphics
        board_none_grafic.battle_list=[[] for i in xrange(6)]
        for i in range(6):
            for j in self.cards_battle[i]:
                board_none_grafic.battle_list[i].append(j.create_card())
    def create_regu_list_players(self,board_none_grafic): #Function that builds lists of the players without graphics
        for i in range(2):
            for j in self.list_players[i]:
                board_none_grafic.list_of_players[i].append(j.create_card())
    def find_attack_option(self,player,board_none_grafic): #Function that returns list that contains none graphics board
        #and in each one of them there is different attacking option
        counter=0
        options=[]
        battle_list=board_none_grafic.list_battle_attack2()
        for i in board_none_grafic.list_of_players[player]:
            for j in battle_list:
                if board_none_grafic.is_full():
                    return options
                elif i.number == j.number:
                    v=copy.deepcopy(board_none_grafic)
                    k=board_none_grafic.find_empty_place2()
                    v.battle_list[k].append(i)
                    del v.list_of_players[player][counter]
                    options.append(v)
                    break
            if len(battle_list)==0:
                v = copy.deepcopy(board_none_grafic)
                k = board_none_grafic.find_empty_place2()

                v.battle_list[k].append(i)
                del v.list_of_players[player][counter]
                options.append(v)
            counter+=1
        return options
    def find_defence_option(self, player,board_none_grafic): #Function that returns list that contains none graphics board
        #and in each one of them there is different defence option
        counter=0
        options = []
        card_to_def=board_none_grafic.find_need_defence()
        if type (card_to_def)==int:
            for i in board_none_grafic.list_of_players[player]:
                if i.check_bigger(board_none_grafic.battle_list[card_to_def][0]):
                    k=copy.deepcopy(board_none_grafic)
                    k.battle_list[card_to_def].append(i)
                    del k.list_of_players[player][counter]
                    options.append(k)
                    counter+=1
        return options
    def recurse_find_card(self, options, player, flag,board_none_grafic): #Function that contains brutforce AI.
        #exit conditions are human player wins returns false, or computer wins returns true.
        #If there is no condition for exit the function will continue the brutforce AI by placing all options recursively
        if len(board_none_grafic.list_of_players[1])==0:
            return True
        if len(board_none_grafic.list_of_players[0]) == 0:
            return False
        for i in options:
            if player==1:
                player2=0
            else:
                player2=1
            if flag==True:
                return self.recurse_find_card(self.find_defence_option(player2,i),player2,False,i)
            else:
                j=i.find_need_defence()
                if type(j)==int:
                    return self.recurse_find_card(self.find_defence_option(player, i), player, False,i)
                else:
                    return self.recurse_find_card(self.find_attack_option(player2, i), player2, True,i)
        if len(options)==0:
            if player == 1:
                player2 = 0
            else:
                player2 = 1
            if flag==True:
                board2=[[] for i in xrange(6)]
                board_none_grafic.battle_list=board2
                return self.recurse_find_card(self.find_attack_option(player2,board_none_grafic), player2, True,board_none_grafic)
            else:
                board_none_grafic.take_cards_from_board(player)
                return self.recurse_find_card(self.find_attack_option(player2,board_none_grafic), player2, True,board_none_grafic)

    #Until here
    def find_this_card(self,card): #Function that gets a card, the function returns the index of the card if it exists, else false
        for i in range(len(self.list_players[1])):
            if card.number==self.list_players[1][i].number and card.shape==self.list_players[1][i].shape:
                return i
        return False
    def list_battle_attack(self): #Function that returns all cards that the battle consist of.
        list_battle = []
        for i in range(6):
            if len(self.cards_battle[i]) == 1:
                list_battle.append(self.cards_battle[i][0])
            elif len(self.cards_battle[i]) == 2:
                list_battle.append(self.cards_battle[i][0])
                list_battle.append(self.cards_battle[i][1])
        return list_battle
    def attack_computer(self, player, dt): #Function that returns cards for attack or clears the board and move the turn
        if player == 0:
            if self.is_empty() == True:
                self.free_cards()
            else:
                self.stuck_the_other()
            return 0
        list_battle = []
        list_battle=self.list_battle_attack()
        b=self.attack_decision(list_battle,player)
        if type(b)==int :
            t=self.find_empty_place()
            self.add_card_to_board(b,t,1,True)
            Clock.schedule_once(partial(self.deffened_computer, 0), 1.5)
        elif b==False:
            if len(self.list_cards) != 0:
                self.take_cards_from_list(0)
            if len(self.list_cards) != 0:
               self.take_cards_from_list(1)
            for i in range(6):
                for j in range(len(self.cards_battle[i])):
                    self.remove_widget(self.cards_battle[i][0])
                    del self.cards_battle[i][0]
            self.cards_battle = [[] for i in xrange(6)]
            self.turn_attack = 0
            self.turn_deffedned = 1
            self.lab1.text = 'attack' + ' ' + str(self.turn_attack + 1)
            self.lab2.text = text = 'defenned' + ' ' + str(self.turn_deffedned + 1)
            Clock.schedule_once(partial(self.attack_computer, 0), 1.5)

    def is_full(self): #Function that checks if the board is full, returns true if full else false
        for i in range(len(self.cards_battle)):
            if len(self.cards_battle[i]) == 0:
                return False
        return True
    def list_end(self): #Function that returns score according the pack of cards
        if len(self.list_cards)>15:
            return 8
        if 5<len(self.list_cards)<15:
            return 4
        return 0
    def check_can_be_in(self,battle_list,card): #Function that returns true if card can take part in battle else false
        #Card can take part if there is a card with same number
        for i in battle_list:
            if card.number==i.number:
                return True
        return False
    def lost_good_one(self): #Function that returns true if there was loss of a good number for the human player
        # (any quzar or non quzar card like Ace, King and queen).
        counter=0
        for j in self.cards_battle:
            if len(j)==2:
                if j[1].flag_quzar==True or j[1].number>=12 and self.list_end()!=0:
                    return True
            counter+=1
        return False
    def attack_decision(self, battle_list,player):#Function that searches card to attack.
        #When there is a pack of cards to take from it searches according tactics, when there isn't it searches by brutforce.
        #Returns number of card if it finds it else false.
       if len(self.list_cards)!=0:
           if self.lost_good_one()==True:
               return False
           score_list=[]
           for i in self.list_players[1]:
               if self.is_empty():
                   score=100-self.how_much_shapes(i)-self.list_end()-i.score*2
                   score_list.append((score,i))
               elif self.check_can_be_in(battle_list,i):
                   score = 100 - self.how_much_shapes(i) - self.list_end()  - i.score*2
                   score_list.append((score, i))
           if len(score_list)!=0:
               max = 0
               for j in range (len(score_list)):
                   if max==0:
                      if score_list[j][0]>max and self.special_condition(score_list[j][1])==False:
                         max=score_list[j]
                   elif score_list[j][0] > max[0] and self.special_condition(score_list[j][1])==False:
                       max = score_list[j]
               if max==0:
                   return False
               k= self.find_this_card(max[1])
               if self.is_empty()==True:
                   return k
               if self.is_empty()==False and max[0]>50:
                    return k
               return False
           else:
               return False
       elif len(self.list_players[1])!=0:
           board_for_requrse = board_for_AI()
           self.build_board(board_for_requrse)
           self.create_regu_list_players(board_for_requrse)
           options=self.find_attack_option(1,board_for_requrse)
           last_options=copy.deepcopy(board_for_requrse)
           last_options.battle_list=[[] for i in xrange(6)]
           need_board_to_win=[]
           if options!=None:
               for i in options:
                   if self.recurse_find_card(self.find_defence_option(0,i),0,False,copy.deepcopy(i))==True:
                       need_board_to_win=i
                       break
           the_card = ' '
           if need_board_to_win==[]:
                return False
           print need_board_to_win,'jjjjjjjjjjjj'
           for i in range(6):
               if len(need_board_to_win.battle_list[i]) == 1:
                   the_card = i
                   break
           b=self.find_this_card(need_board_to_win.battle_list[the_card][0])
           print b,'ppppppp'
           return b
    def is_empty(self): #Function that if the board is empty returns true else returns false
        for i in range(len(self.cards_battle)):
            if len(self.cards_battle[i]) != 0:
                return False
        return True
    def will_answer(self,card): #Function that gets a card and returns if this card will be 100% defended by
        # the human player.
        for i in self.list_known:
            if i.check_bigger(card) and i.flag_quzar==False and i.number<=10:
                return 40
        return 0
    def print_board(self,matrix): #Function that prints any kind of matrix for checking the game.
        for i in matrix:
            for j in i:
                print j.number,j.shape,'kkkkkkkkk'
            print'sssssssssss'
    def end_game_check(self): #Function that checks if there is win condition for any player, returns true if there
        #  is else false
        if len(self.list_cards)==0:
            if len(self.list_players[0])==0 and len(self.list_players[1])==0:
                 self.add_widget(Label(text='draw',pos=(800,800)))
                 return True
            elif len(self.list_players[0])==0 and len(self.list_players[1])!=0:
                 self.add_widget(Label(text='player won', pos=(800, 800)))
                 return True
            elif len(self.list_players[0])!=0 and len(self.list_players[1])==0:
                 self.add_widget(Label(text='computer won', pos=(800, 800)))
                 return True
            return False
        return False

class YourApp(App): # Class that helps to build the screen that contains the game
    def build(self): #Function that returns the Board of the game to be shown on the screen
        self.board = Board()
        return self.board

app = YourApp()
app.run()