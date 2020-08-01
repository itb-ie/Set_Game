import tkinter as tk
from tkinter.ttk import *
from tkinter import filedialog
from ttkthemes import ThemedTk

import random

colors = ["red", "green", "blue"]
fills = ["empty", "medium", "full"]
shapes = ["square", "triangle", "circle"]
numbers = [1, 2, 3]


class Card():
    def __init__(self, color, fill, shape, number):
        self.card = {}
        self.card["color"] = color
        self.card["fill"] = fill
        self.card["shape"] = shape
        self.card["number"] = number

    def get_color(self):
        return self.card["color"]

    def get_fill(self):
        return self.card["fill"]

    def get_shape(self):
        return self.card["shape"]

    def get_number(self):
        return self.card["number"]

    def __str__(self):
        return ("{} {} {} {}".format(self.get_color(), self.get_fill(), self.get_shape(), self.get_number()))

    def get_picture(self):
        nr = 27 * (colors.index(self.get_color())) + \
            9 * (fills.index(self.get_fill())) + \
            3 * (shapes.index(self.get_shape())) + \
            (numbers.index(self.get_number())) + 1
        return nr

class Deck():
    def __init__(self):
        self.cards = []
        for c in colors:
            for f in fills:
                for s in shapes:
                    for n in numbers:
                        self.cards.append(Card(c, f, s, n))

    def shuffle(self):
        random.shuffle(self.cards)

    def draw_card(self):
        return self.cards.pop()

    def draw_12(self):
        cards = []
        for i in range(12):
            cards.append(self.draw_card())
        return cards

    @staticmethod
    def check_set(cards):
        if len(cards) != 3:
            return False
        cards_color = {cards[0].get_color(), cards[1].get_color(), cards[2].get_color()}
        cards_fill = {cards[0].get_fill(), cards[1].get_fill(), cards[2].get_fill()}
        cards_shape = {cards[0].get_shape(), cards[1].get_shape(), cards[2].get_shape()}
        cards_number = {cards[0].get_number(), cards[1].get_number(), cards[2].get_number()}
        if (len(cards_color) == 3) or (len(cards_color) == 1):
            if (len(cards_fill) == 3) or (len(cards_fill) == 1):
                if (len(cards_shape) == 3) or (len(cards_shape) == 1):
                    if (len(cards_number) == 3) or (len(cards_number) == 1):
                        return True
        return False

    def get_three(self, poz, cards):
        if not len(self.cards):
            return False
        cards[poz[0]] = self.draw_card()
        cards[poz[1]] = self.draw_card()
        cards[poz[2]] = self.draw_card()
        return True


class Game():
    def __init__(self, window, deck):
        self.win = window
        self.title = Label(master=self.win, text="Welcome to Set, let's practice to beat Raylooka")
        self.title.grid(row=0, column=0, columnspan=2, padx=20, pady=20)

        self.exit_bt = Button(master=self.win, text="Exit", command=tk.sys.exit)
        self.exit_bt.grid(row=9, column=5, pady = 30, padx=10)

        self.set_bt = Button(master=self.win, text="Check Set", command=self.check_set)
        self.set_bt.grid(row=9, column=0, pady = 30)

        self.status = Label(master=self.win, text="")
        self.status.grid(row=8, column=0, columnspan=2, pady=10)

        self.frame = Frame(master=self.win)
        self.frame.grid(row=1, column=0, columnspan=4, rowspan=5)
        self.score = 0

        self.score_text = Label(master=self.win, text="Score: {}".format(self.score), style="Score.TLabel")
        self.score_text.grid(row=1, column=5, pady=10, padx=10)

        self.hint_bt = Button(master=self.win, text="Hint(-3P)", command=self.show_set)
        self.hint_bt.grid(row=3, column=5, pady=30, padx=10)

        self.pictures = []
        self.cb = []
        self.cb_var = []
        self.deck = deck
        self.cards = deck.draw_12()
        self.display_cards()

    def check_set(self):
        num_set = 0
        poz = []
        for idx,var in enumerate(self.cb_var):
            if var.get():
                poz.append(idx)
                num_set += 1
        if num_set != 3:
            self.status.configure(text="You need to select 3 pictures!")
            for i in poz:
                self.cb_var[i].set(0)
            self.win.after(1000, self.reset_status)
        else:
            print(poz, num_set)
            cards_to_check = [self.cards[poz[0]], self.cards[poz[1]], self.cards[poz[2]]]
            is_set = Deck.check_set(cards_to_check)
            if is_set:
                self.status.configure(text="That was a set. Good job!")
                self.score += 1
                self.update_score()

                # remove the 3 cards and get 3 more
                if not self.deck.get_three(poz, self.cards):
                    self.status.configure(text="No more cards in the deck. Game over!")
                    return

                self.display_cards()
                if not self.get_set():
                    self.status.configure(text="There are no valid sets! Reshuffling")
                    self.win.after(4000, self.reshuffle)
                    return
            else:
                self.status.configure(text="That was not a set. Try again!")
                for i in poz:
                    self.cb_var[i].set(0)
                self.score -= 1
                self.update_score()
            self.win.after(1000, self.reset_status)

    def reset_status(self):
        self.status.configure(text="")

    def update_score(self):
        self.score_text.configure(text="Score: {}".format(self.score))

    def display_cards(self):
        self.pictures = []
        self.cb_var = []
        self.cb = []
        for idx, c in enumerate(self.cards):
            self.pictures.append(tk.PhotoImage(file="cards/" + str(c.get_picture())+".gif"))
            self.cb_var.append(tk.IntVar())
            self.cb.append(Checkbutton(master=self.frame, image=self.pictures[-1], text=str(idx), variable=self.cb_var[-1]))
            self.cb[-1].grid(row=idx//4, column=idx%4, padx=10, pady=10)

    def get_set(self):
        for i in range(12):
            for j in range(i+1, 12):
                for k in range(j+1, 12):
                    cards_to_check = [self.cards[i], self.cards[j], self.cards[k]]
                    is_set = Deck.check_set(cards_to_check)
                    if is_set:
                        return [i,j,k]
        return False

    def show_set(self):
        for c in self.cb_var:
            c.set(0)
        sol = self.get_set()
        self.cb_var[sol[0]].set(1)
        self.cb_var[sol[1]].set(1)
        self.cb_var[sol[2]].set(1)
        self.score -= 4
        self.update_score()

    def reshuffle(self):
        self.deck.cards.extend(self.cards)
        self.deck.shuffle()
        self.cards = self.deck.draw_12()
        self.display_cards()
        self.reset_status()


window = ThemedTk(screenName="Set Game", theme="radiance")
#window.geometry("1200x900")
window.config(bg='#5511AA')
window.resizable(0, 0)

# with ttk we need to configure styles:
style = Style()
style.configure("TButton", font=("Arial", 12, 'bold'), width=25)
style.configure("TLabel", font=("Arial", 15), anchor=tk.CENTER, width=50, foreground="darkblue")
style.configure("Score.TLabel", font=("Arial", 15), anchor=tk.CENTER, width=12, foreground="darkblue")
style.configure("TEntry", font=("Arial", 15), anchor=tk.W)
style.configure("TFrame", background="#111111")

deck = Deck()
deck.shuffle()

g = Game(window, deck)

#print(card)
#print(card.get_picture())


window.mainloop()


