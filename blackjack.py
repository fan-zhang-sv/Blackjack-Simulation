from enum import Enum
import random
from blackjack_player import Move, Player, Dealer

available_cards = []
used_cards = []
player_num = 2
deck_num = 4
players = []
simulation_round = 1000000


class Result(Enum):
    win = 1
    lose = 2
    busted = 3
    blackjack = 4
    even = 5


def init_cards() -> None:
    available_cards.clear()
    used_cards.clear()
    for _ in range(deck_num):
        for num in range(2, 10+1):
            for _ in range(4):
                available_cards.append(str(num))
        
        for _ in range(4):
            available_cards.append('J')
            available_cards.append('Q')
            available_cards.append('K')
            available_cards.append('A')
    
    shuffle_cards(available_cards)


def shuffle_cards(cards) -> None:
    random.shuffle(cards)


def retrieve_used_cards() -> None:
    shuffle_cards(used_cards)
    available_cards.extend(used_cards)
    used_cards.clear()


def get_a_card() -> str:
    return available_cards.pop(0)


def distribute_a_card(player):
    player.receive_a_card(available_cards.pop(0))


def init_hand_for_all() -> str:
    distribute_a_card(dealer)
    for player in players:
        distribute_a_card(player)
    distribute_a_card(dealer)
    for player in players:
        distribute_a_card(player)
    dealer_first_card = dealer.hand[0]
    return dealer_first_card

if __name__ == "__main__":
    init_cards()

    dealer = Dealer()

    players_results = []

    for _ in range(player_num):
        player = Player()
        players.append(player)
        players_results.append([])


    for round in range(simulation_round):
        print((round+1)/simulation_round)
        dealer_first_card = init_hand_for_all()

        for player in players:
            move = player.make_a_move(dealer_first_card)
            while move == Move.hit:
                distribute_a_card(player)
                move = player.make_a_move(dealer_first_card)
        
        move = dealer.make_a_move()
        while move == Move.hit:
            distribute_a_card(dealer)
            move = dealer.make_a_move()

        for idx, player in enumerate(players):
            if player.get_last_move() == Move.busted:
                players_results[idx].append((Result.busted, player.get_final_score()))
            elif player.get_last_move() == Move.blackjack and dealer.last_move != Move.blackjack:
                players_results[idx].append((Result.blackjack, player.get_final_score()))
            else:
                if dealer.get_last_move == Move.busted:
                    players_results[idx].append((Result.win, player.get_final_score()))
                if player.get_final_score() == dealer.get_final_score():
                    players_results[idx].append((Result.even, player.get_final_score()))
                elif player.get_final_score() > dealer.get_final_score():
                    players_results[idx].append((Result.win, player.get_final_score()))
                elif player.get_final_score() < dealer.get_final_score():
                    players_results[idx].append((Result.lose, player.get_final_score()))
            
            used_cards.extend(player.clear_hand())
        used_cards.extend(dealer.clear_hand())

        if len(used_cards) > 30:
            retrieve_used_cards()
    
    # print(players_results[0])
    win = 0
    lose = 0
    even = 0
    bj = 0
    busted = 0
    for result, number in players_results[0]:
        if result == Result.win:
            win+=1
        elif result == Result.lose:
            lose+=1
        elif result == Result.even:
            even+=1
        elif result == Result.blackjack:
            bj+=1
        elif result == Result.busted:
            busted+=1
    
    print("win percentage: ")
    print(win/simulation_round)
    print("lose percentage: ")
    print(lose/simulation_round)
    print("even percentage: ")
    print(even/simulation_round)
    print("blackjack percentage: ")
    print(bj/simulation_round)
    print("busted percentage: ")
    print(busted/simulation_round)

