"""
ICS 31 Lab 8  Problem 1
Author:  UCI_ID: 63139114  Name: Joshua Tavassolikhah
"""
import random

class Card:
    Name   = None
    Value  = None
    
class Bets:
    player_funds = 0
    player_bet = 0

def menu():
    b = Bets()
    b.player_funds = 100
    return b

def makeCard(name:str, value:str) -> Card:
    c = Card()
    c.Name  = name
    c.Value = value
    return c

def select_Sort(Card_Deck:[Card]) -> [Card]:
    new_sorted_deck = []
    
    while len(Card_Deck) > 0:
        min_card = Card_Deck[0]
        min_index = 0
        for check_index in range(len(Card_Deck)):
            if Card_Deck[check_index].Value < min_card.Value:
                min_card = Card_Deck[check_index]
                min_index = check_index
            elif Card_Deck[check_index].Value == min_card.Value:
                if Card_Deck[check_index].Name < min_card.Name:
                    min_card = Card_Deck[check_index]
                    min_index = check_index
        new_sorted_deck.append(min_card)
        del Card_Deck[min_index]    
    return new_sorted_deck

def make_Card_Deck_List(my_deck:[{str:int}]) -> [Card]:
    Card_Deck = []
    for key in my_deck:
        Card_Deck.append(makeCard(key, my_deck[key]))
    new_sorted_deck = select_Sort(Card_Deck)
    return new_sorted_deck

def print_deck(card_deck_list:[Card]):
    for card in card_deck_list:
        print(card.Name,card.Value)
        
def generate_shuffled_deck(full_deck:[Card]):
    shuffle_list = full_deck.copy()
    random.shuffle(shuffle_list)
    return shuffle_list

def drawCard(available_cards:[Card]):
    return available_cards.pop()

def make_standard_Card_Deck_List(my_deck:[{str:int}]) -> [Card]:
    list_of_cards = make_Card_Deck_List(my_deck)
    new_sorted_deck = select_Sort(list_of_cards)
    return new_sorted_deck

def generate_shuffled_deck(full_deck:[Card]) -> [Card]:
    shuffle_list = full_deck.copy()
    random.shuffle(shuffle_list)
    return shuffle_list

def createStartingHand(available_cards:[Card],num_to_draw:int) -> [Card]:
    num_of_draw_cards = []
    while num_to_draw > 0:
        num_of_draw_cards.append(drawCard(available_cards))
        num_to_draw = num_to_draw - 1
    return num_of_draw_cards

def print_Hand(card_list:[Card]):
    for card in card_list:
        if card.Value == 11:
            print(card.Name + " with a value of " + str(card.Value) + " or 1")
        else:
            print(card.Name + " with a value of " + str(card.Value))
        
def eval_Hand(card_list:[Card]) -> int:
    total = 0
    for card in card_list:
        total += card.Value
    if total > 21:
        total = 0
        for card in card_list:
            if card.Value == 11:
                card.Value -= 10
            total+=card.Value
        return total
    return total

def print_player_hand(player_hand:[Card]):
    total = eval_Hand(player_hand)
    print("\nYour hand contains: ")
    print_Hand(player_hand)
    print("\nFor a total value of:",total,"\n")

def print_computer_hand(computer_hand:[Card]):
    total = eval_Hand(computer_hand)
    print("The Friend Computer's hand contains:\n")
    print_Hand(computer_hand)
    print("For a total value of",total)
    
def getH_or_SChoice() -> str:
    choice = getString("Would you like to Hit(H) or Stay(S)? ",["H","S"])
    return choice

def stayOrHit(player_hand:[Card],available_cards:[Card]) -> bool:
    choice = getH_or_SChoice()
    if choice == "H":
        card = drawCard(available_cards)
        if card.Value == 11:
            print("\nYou drew",card.Name,"which has a value of",card.Value, "or 1")
        else:
            print("\nYou drew",card.Name,"which has a value of",card.Value)
        player_hand.append(card)
        total = eval_Hand(player_hand)
        print("You now have a total value of",total)
        if total > 21:
            return False
        else:
            return True

def getBetChoice() -> str:
    choice = getString("Would you like to Raise(R) or Stay(S)? ",["R","S"])
    return choice

def getBetAmount(available_for_bet:int) -> int:
    while True:
        try:
            b = int(input("How much would you like to raise by: "))
            if b < 0:
                print("The bet cannot be a negative number, please try again")
            elif b <= available_for_bet:
                return b
            elif b > available_for_bet:
                print("That bet needs to be <= $"+str(available_for_bet))
        except ValueError:

            print("Enter a number please")

def betting(bets:Bets) -> bool:
    print("Your current bet is $"+str(bets.player_bet)+" of your $"+str(bets.player_funds) + " funds")
    if bets.player_bet == bets.player_funds:
        return
    print("You can increase your bet by at most $"+str(bets.player_funds - bets.player_bet))
    choice = getBetChoice()
    if choice == "R":
        bet = getBetAmount(bets.player_funds)
        bets.player_bet += bet
        print("Your bet has been increased to $"+str(bets.player_bet))
        print("You can increase your bet by at most $" + str((bets.player_funds - bets.player_bet)))
    elif choice == "S":
        return False
        
    
def computerTurn(computer_hand:[Card],available_cards:[Card]) -> bool:
    total = eval_Hand(computer_hand)
    if total < 17:
        print("\nThe Friend Computer Hits.")
        computer_hand.append(drawCard(available_cards))
        total = eval_Hand(computer_hand)
        if total > 21:
            return False
        else:
            return True
    elif 17 <= total <= 21:
        print("The Friend Computer stays")
   

def game_run(full_deck:[{str:int}]) -> [Card]:
    sorted_deck = make_standard_Card_Deck_List(full_deck)
    shuffle_list = generate_shuffled_deck(sorted_deck)
    player_list = createStartingHand(shuffle_list,2)
    print_player_hand(player_list)
    cpu_list = createStartingHand(shuffle_list,2)
    return shuffle_list,player_list,cpu_list

def you_won(Bet:Bets,cpu_list:[Card]):
    print("The computer has bust. You win this round !!")
    print("Your bet of $"+str(Bet.player_bet)+" has been added to your funds !!")
    Bet.player_funds += Bet.player_bet
    print("You now have $"+str(Bet.player_funds))
    print("Now that the round has ended, the Friend Computer's hand will be revealed")
    print_computer_hand(cpu_list)

def you_lost(Bet:Bets,cpu_list:[Card]):
    print("\nThe Friend Computer Triumphed!\nThe Friend Computer had a better hand this time.")
    print("Your funds have been decreased by your bet size")
    Bet.player_funds -= Bet.player_bet
    print("You now have $"+str(Bet.player_funds))
    print("Now that the round has ended, the Friend Computer's hand will be revealed")
    print_computer_hand(cpu_list)
    
def lose_all_funds():
    print("\nAlas you have run out of money.")
    print("We hope you come back and play again soon!")
    print("The Friend Computer always appreciates financial contributions!")

def both_stay_message(player_list:[Card],cpu_list:[Card]):
    print("\nALl players have chosen to stay, so we will reveal hands")
    player_list_total = eval_Hand(player_list)
    cpu_list_total = eval_Hand(cpu_list)
    print("Your hand has a final value of",player_list_total)
    print("The Friend Computer has a final value of",cpu_list_total)

def tie(Bet:Bets,cpu_list:[Card]):
    print("What? You have tied with the Friend Computer?!?!?")
    print("Alright mortal, I will grant you the pot....this time.....")
    print("The Friend Computer has graciously and generously awarded you")
    print("Your bet has been added to your funds")
    Bet.player_funds += Bet.player_bet
    print("You now have $"+str(Bet.player_funds))
    print("Now that the round has ended, the Friend Computer's hand will be revealed.")
    print_computer_hand(cpu_list)

def both_stay(player_list:[Card],cpu_list:[Card],Bet:Bets) -> bool:

    both_stay_message(player_list,cpu_list)
    
    if eval_Hand(player_list) > eval_Hand(cpu_list):
        you_won(Bet,cpu_list)
        return True
    elif eval_Hand(player_list) < eval_Hand(cpu_list):
        you_lost(Bet,cpu_list)
        return True
    elif eval_Hand(player_list) == eval_Hand(cpu_list):
        tie(Bet,cpu_list)
        return True
        
    
def runRound(full_deck:[{str:int}],funds:int):
    shuffle_list,player_list,cpu_list = game_run(full_deck)
    while True:
        bet = betting(funds)
        if bet == False:
            print("Your bet is unchanged and remains at $"+str(funds.player_bet))
        cpu_turn = computerTurn(cpu_list,shuffle_list)
        if cpu_turn == False:
            you_won(funds,cpu_list)
            break
        stay_or_hit = stayOrHit(player_list,shuffle_list)
        if stay_or_hit == False:
            you_lost(funds,cpu_list)
            break
        if stay_or_hit == None:
            print("You chose to stay/skip this turn")
        if stay_or_hit == None and cpu_turn == None:
            bothStay = both_stay(player_list,cpu_list,funds)
            if bothStay == True:
                break
            
def getString(prompt:str, options:list) -> str:
    choice = input(prompt).upper().strip()
    while not choice in options:
        print("Invalid input, please enter ", end = "")
        if len(options) == 2:
            print(options[0], "or", options[1])
        else:
            for option in options:
                if option != options[-1]:
                    print(option, end = "," )
                else:
                    print( " or" , option)
        choice = input(prompt).upper().strip()
    return choice

def runGame(full_deck:[{str:int}],Game_Money:int):
    while True:
        Game_Money.player_bet = 0
        runRound(full_deck,Game_Money)
        if Game_Money.player_funds == 0:
            lose_all_funds()
            break
        print("\nThe Friend Computer would like to play another round!")
        choice = cont_or_quit()
        if choice == "Q":
            print("\nThank you for playing!\nEnjoy your remaining funds of $"+str(Game_Money.player_funds)+"!")
            break
    
def deck() -> dict:
    official_deck = {
    "Ace of Spades" : 11,
    "Two of Spades" : 2,
    "Three of Spades" : 3,
    "Four of Spades" : 4,
    "Five of Spades" : 5,
    "Six of Spades" : 6,
    "Seven of Spades" : 7,
    "Eight of Spades" : 8,
    "Nine of Spades" : 9,
    "Ten of Spades" : 10,
    "Jack of Spades" : 10,
    "Queen of Spades" : 10,
    "King of Spades" : 10,
    "Ace of Hearts" : 11,
    "Two of Hearts" : 2,
    "Three of Hearts" : 3,
    "Four of Hearts" : 4,
    "Five of Hearts" : 5,
    "Six of Hearts" : 6,
    "Seven of Hearts" : 7,
    "Eight of Hearts" : 8,
    "Nine of Hearts" : 9,
    "Ten of Hearts" : 10,
    "Jack of Hearts" : 10,
    "Queen of Hearts" : 10,
    "King of Hearts" : 10,
    "Ace of Diamonds" : 11,
    "Two of Diamonds" : 2,
    "Three of Diamonds" : 3,
    "Four of Diamonds" : 4,
    "Five of Diamonds" : 5,
    "Six of Diamonds" : 6,
    "Seven of Diamonds" : 7,
    "Eight of Diamonds" : 8,
    "Nine of Diamonds" : 9,
    "Ten of Diamonds" : 10,
    "Jack of Diamonds" : 10,
    "Queen of Diamonds" : 10,
    "King of Diamonds" : 10,
    "Ace of Clubs" : 11,
    "Two of Clubs" : 2,
    "Three of Clubs" : 3,
    "Four of Clubs" : 4,
    "Five of Clubs" : 5,
    "Six of Clubs" : 6,
    "Seven of Clubs" : 7,
    "Eight of Clubs" : 8,
    "Nine of Clubs" : 9,
    "Ten of Clubs" : 10,
    "Jack of Clubs" : 10,
    "Queen of Clubs" : 10,
    "King of Clubs" : 10}

    return official_deck

def intro_message():
    print("Hello and Welcome to the Variety Bot's BlackJack Table!")
    print("Your goal is to get a higher card total than me!")
    print("Whoever is closer to 21 wins!")
    print("Note: Ace defaults to 11, but will change to 1, should you exceed 21.")
    print("Also beware that I NEVER turn down a bet and I am nfinitely wealthy ;)")
    print("Let's get started")

def cont_or_quit() -> str:
    choice = getString("Would you like to Continue and Play Another Round (C) or Quit(Q)? ", ["C", "Q",])
    return choice
    
def main():
    intro_message()
    full_deck = deck()
    funds = menu()
    runGame(full_deck,funds)
    
if __name__ == "__main__":
    main()

