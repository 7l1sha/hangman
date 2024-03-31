import random
from tkinter import *
from tkinter import messagebox

score = 0

def close():
    global run
    answer = messagebox.askyesno('ALERT', 'YOU WANT TO EXIT THE GAME?')
    if answer:
        run = False
        root.destroy()

def reset_game():
    global count, win_count, guessed_letters, score
    count = 0
    win_count = 0
    guessed_letters = set()
    score = 0
    typed_label.config(text="")
    draw_hangman(0)
    draw_word()
    
def draw_word():
    global selected_word, score
    x = 250
    word_display = ""
    for letter in selected_word:
        x += 60
        if letter in guessed_letters:
            word_display += letter + " "
        else:
            word_display += "_ "
    word_label.config(text=word_display)

    if set(selected_word) <= guessed_letters:
        score += 1
        score_label.config(text=f'SCORE: {score}')
        if messagebox.askyesno('GAME OVER', 'YOU WON!\nWANT TO PLAY AGAIN?'):
            reset_game()
        else:
            close()

def draw_hangman(step):
    hangman_label.config(image=hangman_images[step])

def check(letter):
    global count
    if letter in guessed_letters:
        return  # Ignore repeated letters
    guessed_letters.add(letter)
    typed_label.config(text=typed_label.cget("text") + letter + " ")
    if letter in selected_word:
        draw_word()
    else:
        count += 1
        draw_hangman(count)
        if count == 6:
            if messagebox.askyesno('GAME OVER', 'YOU LOST!\nWANT TO PLAY AGAIN?'):
                reset_game()
            else:
                close()

# main loop
run = True
while run:
    root = Tk()
    root.geometry('905x700')
    root.title('HANG MAN')
    root.config(bg='#E7FFFF')
    count = 0
    win_count = 0
    guessed_letters = set()

    # choosing word
    with open('words.txt', 'r') as file:
        words = file.readlines()
        selected_word = random.choice(words).strip().lower()

    # hangman images
    hangman_images = [PhotoImage(file=f'h{i}.png') for i in range(1, 8)]
    hangman_label = Label(root, bg="#E7FFFF")
    hangman_label.place(x=300, y=-50)

    # word label
    word_label = Label(root, text="", bg="#E7FFFF", font=("arial", 40))
    word_label.place(x=250, y=450)

    # exit button
    exit_button = Button(root, text="EXIT", command=close)
    exit_button.place(x=770, y=10)

    # score label
    score_label = Label(root, text=f'SCORE: {score}', bg="#E7FFFF", font=("arial", 25))
    score_label.place(x=10, y=10)

    # typed letters label
    typed_label = Label(root, text="", bg="#E7FFFF", font=("arial", 20))
    typed_label.place(x=10, y=70)

    # bind key press event
    def key_press(event):
        letter = event.char.lower()
        if letter.isalpha():
            check(letter)

    root.bind('<Key>', key_press)
    root.mainloop()
