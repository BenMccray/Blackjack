import random

class Card:
    """Represents a single card."""
    def __init__(self, rank, suit):
        self.rank = rank
        self.suit = suit

    def __str__(self):
        return f"{self.suit}{self.rank}"

class Shoe:
    """Represents a shoe of cards."""
    ranks = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']
    suits = ['♠', '♣', '♥', '♦']
    shoe = []

    def __init__(self, deck_count=6):
        self.deck_count = deck_count
        self.shuffle(deck_count)

    def is_empty(self):
        """Check if the shoe is empty."""
        return len(self.shoe) == 0

    def shuffle(self, deck_count):
        """Shuffle the shoe defaulting to 6 decks."""
        for _ in range(deck_count):
            for suit in self.suits:
                for rank in self.ranks:
                    self.shoe.append(Card(rank, suit))
        random.shuffle(self.shoe)

    def print_shoe(self):
        """Print the contents of the shoe."""
        print("Shoe contains:")
        for card in self.shoe:
            print(card, end=' ')
        print()

    def deal_card(self):
        """Deal a card from the shoe."""
        if self.is_empty():
            self.shuffle(self.deck_count)
            print("Shoe was empty, reshuffled.")
        return self.shoe.pop()


class Hand:
    """Represents a hand of cards."""
    def __init__(self):
        self.cards = []

    def add_card(self, card):
        """Add a card to the hand."""
        self.cards.append(card)

    def calculate_value(self):
        """Calculate the value of the hand."""
        value = 0
        aces = 0
        for card in self.cards:
            if card.rank in ['J', 'Q', 'K']:
                value += 10
            elif card.rank == 'A':
                value += 11
                aces += 1
            else:
                value += int(card.rank)
        # Adjust for Aces if value is over 21
        while value > 21 and aces:
            value -= 10
            aces -= 1
        return value

    def __str__(self):
        return f"[{', '.join(str(card) for card in self.cards)}] (Value: {self.calculate_value()})"

class Player:
    """Represents the player."""
    def __init__(self, balance=100):
        self.balance = balance
        self.hand = Hand()

    def place_bet(self):
        """Ask the player to place a bet."""
        while True:
            try:
                bet = int(input(f"Your current balance is ${self.balance}. Place your bet: $"))
                if bet < 1:
                    print("Bet must be at least $1.")
                elif bet > self.balance:
                    print("You don't have enough money to place that bet.")
                else:
                    return bet
            except ValueError:
                print("Invalid input. Please enter a number.")

    def reset_hand(self):
        """Reset the player's hand for a new round."""
        self.hand = Hand()

class Dealer:
    """Represents the dealer."""
    def __init__(self):
        self.hand = Hand()

    def reset_hand(self):
        """Reset the dealer's hand for a new round."""
        self.hand = Hand()

    def play_turn(self, shoe):
        """Dealer's turn to hit until reaching 17 or higher."""
        while self.hand.calculate_value() < 17:
            self.hand.add_card(shoe.deal_card())

class Table:
    """Manages the Blackjack table."""
    def __init__(self):
        self.shoe = Shoe()
        self.player = Player()
        self.dealer = Dealer()

    def display_hands(self, hide_dealer_card=True):
        """Display the player's and dealer's hands."""
        print("\nYour hand:")
        print(self.player.hand)
        print("\nDealer's hand:")
        if hide_dealer_card:
            print(f"[Hidden, {', '.join(str(card) for card in self.dealer.hand.cards[1:])}]")
        else:
            print(self.dealer.hand)

    def player_turn(self):
        """Player's turn to hit or stand."""
        while True:
            self.display_hands()
            action = input("Do you want to hit or stand? (h/s): ").lower()
            if action == 'h':
                self.player.hand.add_card(self.shoe.deal_card())
                if self.player.hand.calculate_value() > 21:
                    print("\nYour hand:")
                    print(self.player.hand)
                    print("Bust! You went over 21.")
                    return False
            elif action == 's':
                return True
            else:
                print("Invalid input. Please enter 'h' to hit or 's' to stand.")

    def determine_winner(self):
        """Determine the winner of the table."""
        player_value = self.player.hand.calculate_value()
        dealer_value = self.dealer.hand.calculate_value()

        if player_value > 21:
            return "Dealer wins! You busted."
        elif dealer_value > 21:
            return "You win! Dealer busted."
        elif player_value > dealer_value:
            return "You win!"
        elif dealer_value > player_value:
            return "Dealer wins!"
        else:
            return "It's a tie!"

    def play_round(self):
        """Play a single round of Blackjack."""
        bet = self.player.place_bet()
        self.player.balance -= bet

        # Deal initial cards
        self.player.hand.add_card(self.shoe.deal_card())
        self.dealer.hand.add_card(self.shoe.deal_card())
        self.player.hand.add_card(self.shoe.deal_card())
        self.dealer.hand.add_card(self.shoe.deal_card())

        # Player's turn
        if self.player_turn():
            # Dealer's turn
            print("\nDealer's turn:")
            self.dealer.play_turn(self.shoe)
            self.display_hands(hide_dealer_card=False)

            # Determine the winner
            result = self.determine_winner()
            print(f"\n{result}")

            # Update player's balance
            if "You win" in result:
                self.player.balance += bet * 2
                print(f"You won ${bet * 2}!")
            elif "It's a tie" in result:
                self.player.balance += bet
                print("It's a tie. Your bet is returned.")
            else:
                print(f"You lost ${bet}.")
        else:
            print(f"You lost ${bet}.")

    def play_table(self):
        """Main table loop."""
        print("Welcome to Blackjack!")
        print("Dealer hits on 16 and stands on 17.")
        while self.player.balance > 0:
            self.play_round()
            if self.player.balance == 0:
                print("\nYou're out of money! Game over.")
                break
            play_again = input("\nDo you want to play another round? (y/n): ").lower()
            if play_again != 'y':
                print(f"\nThanks for playing! You leave with ${self.player.balance}.")
                break
            # Reset hands for a new round
            self.player.reset_hand()
            self.dealer.reset_hand()

# Start the table
if __name__ == "__main__":
    table = Table()
    table.play_table()
