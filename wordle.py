import ttkbootstrap as ttk
import requests
import json
from tkinter import messagebox


# main class
class App(ttk.Window):
    def __init__(self) -> None:
        super().__init__(themename="vapor")
        # window parameters
        self.geometry("1000x800")
        self.resizable(False, False)
        self.title("Wordle")

        # attempt counter
        self.attempt = 0

        # word draw using API
        r = requests.get("https://random-word-api.vercel.app/api?words=1&length=5")
        self.word = r.text[2:-2]
        self.word_list = list(self.word)

        # widgets - six rows (5 inputs each)
        self.frame1 = Frame(self, self.word)
        self.frame2 = Frame(self, self.word)
        self.frame3 = Frame(self, self.word)
        self.frame4 = Frame(self, self.word)
        self.frame5 = Frame(self, self.word)
        self.frame6 = Frame(self, self.word)

        self.frames = [self.frame1, self.frame2, self.frame3, self.frame4, self.frame5, self.frame6]
        self.frame1.e1.configure(state="active")  # activates first entry field

        # layout - grid configuration and widgets placement
        self.rowconfigure([0, 1, 2, 3, 4, 5, 6, 7], weight=1, uniform="a")
        self.columnconfigure(0, weight=2, uniform="a")
        self.columnconfigure(1, weight=5, uniform="a")
        self.columnconfigure(2, weight=2, uniform="a")

        self.frame1.grid(row=1, column=1, sticky="news")
        self.frame2.grid(row=2, column=1, sticky="news")
        self.frame3.grid(row=3, column=1, sticky="news")
        self.frame4.grid(row=4, column=1, sticky="news")
        self.frame5.grid(row=5, column=1, sticky="news")
        self.frame6.grid(row=6, column=1, sticky="news")

    # activates next row and end game if attempts ended
    def next_row(self) -> None:
        if self.attempt < 5:
            self.attempt += 1
            self.frames[self.attempt].e1.configure(state="active")
            self.frames[self.attempt].e1.focus_set()
        else:
            self.frame6.lose()


# class representing each row of entries
class Frame(ttk.Frame):
    def __init__(self, a, w) -> None:
        super().__init__()
        self.a = a  # referencing App class
        self.word = w  # random word

        # layout - grid configuration and widgets placement
        self.rowconfigure(0, weight=1, uniform="f")
        self.columnconfigure([0, 1, 2, 3, 4], weight=1, uniform="f")

        self.e1 = ttk.Entry(self,
                            width=2,
                            font=("Franklin Gothic Demi", 50),
                            justify="center",
                            state="disabled",
                            bootstyle="primary"
                            )

        self.e2 = ttk.Entry(self,
                            width=2,
                            font=("Franklin Gothic Demi", 50),
                            justify="center",
                            state="disabled",
                            bootstyle="primary"
                            )

        self.e3 = ttk.Entry(self,
                            width=2,
                            font=("Franklin Gothic Demi", 50),
                            justify="center",
                            state="disabled",
                            bootstyle="primary"
                            )

        self.e4 = ttk.Entry(self,
                            width=2,
                            font=("Franklin Gothic Demi", 50),
                            justify="center",
                            state="disabled",
                            bootstyle="primary"
                            )

        self.e5 = ttk.Entry(self,
                            width=2,
                            font=("Franklin Gothic Demi", 50),
                            justify="center",
                            state="disabled",
                            bootstyle="primary"
                            )

        self.es = (self.e1, self.e2, self.e3, self.e4, self.e5)

        self.e1.grid(row=0, column=0, sticky="news")
        self.e2.grid(row=0, column=1, sticky="news")
        self.e3.grid(row=0, column=2, sticky="news")
        self.e4.grid(row=0, column=3, sticky="news")
        self.e5.grid(row=0, column=4, sticky="news")

        # actions binding
        self.e1.bind("<KeyRelease>", lambda x: self.check_len(self.e1, 0))
        self.e2.bind("<KeyRelease>", lambda x: self.check_len(self.e2, 1))
        self.e3.bind("<KeyRelease>", lambda x: self.check_len(self.e3, 2))
        self.e4.bind("<KeyRelease>", lambda x: self.check_len(self.e4, 3))
        self.e5.bind("<KeyRelease>", lambda x: self.check_len(self.e5, 4))

    # moves to the next activated entry in row
    def check_len(self, e, n) -> None:
        if len(e.get()) > 1:  # ensures only one character per entry
            e.delete(1, "end")

        if len(e.get()) == 1 and n < 4:
            self.es[n+1].configure(state="active")
            self.es[n+1].focus_set()

        if n == 4 and self.word_check():  # moves cursor to next row if word exist
            self.a.next_row()
            self.letters_check()
        elif n == 4 and not self.word_check():  # colors all entries and after 1000ms calls clear function
            self.e1.configure(bootstyle="danger")
            self.e2.configure(bootstyle="danger")
            self.e3.configure(bootstyle="danger")
            self.e4.configure(bootstyle="danger")
            self.e5.configure(bootstyle="danger")
            self.after(1000, lambda: self.clear())

    # checks correctness of letters (position and presence).
    def letters_check(self) -> None:
        word = self.e1.get() + self.e2.get() + self.e3.get() + self.e4.get() + self.e5.get()
        for i, w in enumerate(word):
            if w == self.word[i]:
                self.es[i].configure(bootstyle="success")
                self.a.word_list[i] = None

        for i, w in enumerate(word):
            if w in self.a.word_list:
                self.es[i].configure(bootstyle="warning")
                self.a.word_list[self.a.word_list.index(w)] = None

        if word == self.word:
            self.win()

    # clears all entries in row and places cursor on first entry
    def clear(self) -> None:
        self.e1.delete(0, 1)
        self.e2.delete(0, 1)
        self.e3.delete(0, 1)
        self.e4.delete(0, 1)
        self.e5.delete(0, 1)

        self.e1.configure(bootstyle="primary")
        self.e2.configure(bootstyle="primary")
        self.e3.configure(bootstyle="primary")
        self.e4.configure(bootstyle="primary")
        self.e5.configure(bootstyle="primary")

        self.e2.configure(state="disabled")
        self.e3.configure(state="disabled")
        self.e4.configure(state="disabled")
        self.e5.configure(state="disabled")

        self.e1.focus_set()

    # check if word exist
    def word_check(self) -> bool:
        word = self.e1.get() + self.e2.get() + self.e3.get() + self.e4.get() + self.e5.get()
        r = requests.get(f"https://api.dictionaryapi.dev/api/v2/entries/en/{word}")
        if type(json.loads(r.text)) == list:
            return True
        else:
            return False
    
    # disables all entries and shows pop-up that displays win message
    def win(self) -> None:
        for i in self.a.winfo_children():
            for j in i.winfo_children():
                j.configure(state="disabled")
        messagebox.showinfo("Wygrana", "Gratulacje!")

    # disables all entries and shows pop-up that displays lose message and random word
    def lose(self) -> None:
        for i in self.a.winfo_children():
            for j in i.winfo_children():
                j.configure(state="disabled")
        messagebox.showinfo("Przegrana", f"Szukane słowo to {self.a.word}")


if __name__ == '__main__':
    app = App()
    app.mainloop()
