from enum import Enum
from typing import List

class Move(Enum):
    hit = 1
    stand = 2
    busted = 3
    blackjack = 4


class Human():

    def __init__(self) -> None:
        self.hand = []
        self.scores = [0]
        self.last_move = None


    def clear_hand(self) -> List[str]:
        hand_snapshot = self.hand[:]
        self.hand.clear()
        self.scores = [0]
        # print(hand_snapshot)
        return hand_snapshot

    
    def receive_a_card(self, card):
        self.hand.append(card)
        self.update_scores(card)
    

    def update_scores(self, card) -> None:

        def add_for_all(lst, num) -> List[int]:
            return list(map(lambda x:x+num, lst))

        if card.isdigit():
            self.scores = add_for_all(self.scores, int(card))
        else:
            if card in ('J', 'Q', 'K'):
                self.scores = add_for_all(self.scores, 10)
            else:
                # card is Ace
                scores_snapshot = self.scores[:]
                self.scores.clear()
                self.scores.extend(add_for_all(scores_snapshot, 1))
                self.scores.extend(add_for_all(scores_snapshot, 11))


    def get_final_score(self) -> int:
        self.scores.sort(reverse=True)
        for score in self.scores:
            if score <= 21:
                return score
        return self.scores[-1]

    
    def get_last_move(self) -> Move:
        return self.last_move


class Player(Human):

    def __init__(self, stand_threshold=16, dealer_hit_threshold=4) -> None:
        super().__init__()
        self.stand_threshold = stand_threshold
        self.dealer_hit_threshold = dealer_hit_threshold


    def make_a_move(self, dealers_card) -> Move:
        final_score = self.get_final_score()

        if final_score > 21:
            # user exceeded 21, lose automatically
            self.last_move = Move.busted
            return Move.busted

        if final_score == 21:
            # blackjack win
            self.last_move = Move.blackjack
            return Move.blackjack

        if dealers_card.isdigit() and int(dealers_card) <= self.dealer_hit_threshold:
            # wait for dealer to hit
            self.last_move = Move.stand
            return Move.stand

        if final_score >= self.stand_threshold:
            # entered safe range
            self.last_move = Move.stand
            return Move.stand
        
        self.last_move = Move.hit

        return Move.hit



class Dealer(Human):

    def __init__(self, stand_threshold=17) -> None:
        super().__init__()
        self.stand_threshold = stand_threshold


    def make_a_move(self) -> Move:
        final_score = self.get_final_score()

        if final_score > 21:
            # user exceeded 21, lose automatically
            self.last_move = Move.busted
            return Move.busted

        if final_score == 21:
            # blackjack win
            self.last_move = Move.blackjack
            return Move.blackjack

        if final_score >= self.stand_threshold:
            # entered safe range
            self.last_move = Move.stand
            return Move.stand
        
        self.last_move = Move.hit
        return Move.hit


if __name__ == "__main__":

    dealer = Dealer()
    dealer.receive_a_card('A')
    dealer.receive_a_card('A')
    dealer.make_a_move()
    print(dealer.get_last_move())
    print(dealer.get_final_score())

    player = Player()
    player.receive_a_card('8')
    player.receive_a_card('J')
    player.make_a_move('A')
    print(player.get_last_move())
    print(player.get_final_score())

