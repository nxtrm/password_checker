import customtkinter
import random
import re

customtkinter.set_appearance_mode("dark")
customtkinter.set_default_color_theme("dark-blue")

app = customtkinter.CTk()
app.geometry("360x750")
app.title("Password generator")

symbols = 'ABCDEFGHIJKLMONPQRSTUVWXYZabcdefghijklmnopqrstuvwqxyz0123456789!$%^&*()_-+='
keyboard = ["qwertyuiop", "asdfghjkl", "zxcvbnm"]
names = ["Uppercase letters", "Lowercase letters",
         "Digits", "Symbols", "No consecutive letters"]
         
triples = []
for row in keyboard:
    triples.extend(row[i:i + 3] for i in range(len(row) - 2))


def main_menu():

    def check_onClick():
        main_fr.forget()
        check_menu(wrong)

    def generate_onClick():
        main_fr.forget()
        password, score = generate_password()
        while score <= 25:
            password, score = generate_password()
        gen_main(password)

    main_fr = customtkinter.CTkFrame(master=app)
    main_fr.pack(pady=10, padx=10, fill="both", expand=True)

    title_lab = customtkinter.CTkLabel(
        master=main_fr, text="Password Generator", font=customtkinter.CTkFont(size=30, weight="bold"))
    title_lab.pack(pady=100, padx=10)

    check_but = customtkinter.CTkButton(master=main_fr, command=check_onClick, text="Check password", font=customtkinter.CTkFont(
        size=20), height=40, hover_color=("gray70", "gray30"), width=200)
    check_but.pack(pady=15, padx=10)

    gen_but = customtkinter.CTkButton(master=main_fr, command=generate_onClick, text="Generate password", font=customtkinter.CTkFont(
        size=20), height=40, hover_color=("gray70", "gray30"), width=200)
    gen_but.pack(pady=15, padx=10)

    quit_but = customtkinter.CTkButton(master=main_fr, command=app.destroy, text="Quit", font=customtkinter.CTkFont(
        size=20), height=40, hover_color=("gray70", "gray30"), width=200)
    quit_but.pack(pady=15, padx=10)

    wrong = False


def check_menu(wrong):

    def subm_but_onClick():
        check_fr.forget()
        password = pass_entr.get()

        check_fr.forget()
        check_main(password)

    check_fr = customtkinter.CTkFrame(master=app)
    check_fr.pack(pady=10, padx=10, fill="both", expand=True)

    title_lab = customtkinter.CTkLabel(
        master=check_fr, text="Password Checker", font=customtkinter.CTkFont(size=30, weight="bold"))
    title_lab.pack(pady=40, padx=10)

    if wrong == True:
        warning_lab = customtkinter.CTkLabel(
            master=check_fr, text="Password not matching the requirements", font=customtkinter.CTkFont(size=10), text_color="red")
        warning_lab.pack(pady=10, padx=10)

    pass_entr = customtkinter.CTkEntry(
        master=check_fr, placeholder_text="Enter the password to check", width=200)
    pass_entr.pack(padx=10, pady=10)

    subm_but = customtkinter.CTkButton(master=check_fr, command=subm_but_onClick, text="Submit", font=customtkinter.CTkFont(
        size=20), height=40, hover_color=("gray70", "gray30"), width=200)
    subm_but.pack(pady=15, padx=10)


def check_main(password):

    def back_to_main_menu_onClick():
        check_fr1.forget()
        check_fr2.forget()
        main_menu()

    check_fr1 = customtkinter.CTkFrame(master=app)
    check_fr1.pack(pady=10, padx=10, fill="both", expand=True)

    title1_lab = customtkinter.CTkLabel(
        master=check_fr1, text="Password Checker", font=customtkinter.CTkFont(size=30, weight="bold"), )
    title1_lab.pack(pady=30, padx=10)

    password_lab = customtkinter.CTkLabel(
        master=check_fr1, text=password, font=customtkinter.CTkFont(size=20, weight="bold"))
    password_lab.pack(pady=10, padx=10)

    check_fr2 = customtkinter.CTkFrame(master=check_fr1)
    check_fr2.pack(pady=20, padx=10, fill="both", expand=True)

    score, checks = score_calculator(password)
    i = 0
    for check in checks:
        if check == True:
            check_txt = customtkinter.CTkTextbox(master=check_fr2, font=customtkinter.CTkFont(
                size=15), text_color="green", activate_scrollbars=False, height=30, width=300, border_spacing=5)
            check_txt.insert("0.0", names[i])
            check_txt.insert("0.10", "✅             ")
            check_txt.pack(pady=10, padx=5)
        else:
            check_txt = customtkinter.CTkTextbox(master=check_fr2, font=customtkinter.CTkFont(
                size=15), text_color="red", activate_scrollbars=False, height=30, width=300, border_spacing=5)
            check_txt.insert("0.0", names[i])
            check_txt.insert("0.10", "❎             ")
            check_txt.pack(pady=10, padx=5)
        i = i+1

    if score > 20:
        strength = "strong"
        color = "green"
        bar_val = 1
    elif 0 < score < 20:
        strength = "medium"
        color = "yellow"
        bar_val = ((score-0)*(1-0))/(20)
    else:
        strength = "weak"
        color = "red"
        bar_val = 0

    strength_bar = customtkinter.CTkProgressBar(
        master=check_fr2, progress_color=color, width=300)
    strength_bar.set(bar_val)
    strength_bar.pack(pady=10, padx=10)

    score_lab = customtkinter.CTkLabel(master=check_fr2, text="Score: "+str(
        score), font=customtkinter.CTkFont(size=25, weight="bold"))
    score_lab.pack(pady=10, padx=10)

    strength_lab = customtkinter.CTkLabel(
        master=check_fr2, text="Strength: "+strength, font=customtkinter.CTkFont(size=25, weight="bold"))
    strength_lab.pack(pady=20, padx=10)

    back_to_main_menu_but = customtkinter.CTkButton(master=check_fr2, command=back_to_main_menu_onClick, text="Main menu", font=customtkinter.CTkFont(
        size=20), height=40, hover_color=("gray70", "gray30"), width=200)
    back_to_main_menu_but.pack(pady=15, padx=10)


def score_calculator(password):
    score = len(password)
    upper = False
    lower = False
    digit = False
    symbol = False
    no_consecutive = True

    if re.search("[A-Z]", password):
        upper = True
        score += 5
    if re.search("[a-z]", password):
        lower = True
        score += 5
    if re.search("[0-9]", password):
        digit = True
        score += 5
    if re.search("[=!@#$%_^&*+()-]", password):
        symbol = True
        score += 5
    if upper and lower and digit and symbol:
        score += 10

    if upper and lower and not digit and not symbol:
        score -= 5
    if not upper and not lower and digit and not symbol:
        score -= 5
    if not upper and not lower and not digit and symbol:
        score -= 5

    for triple in triples:
        if triple in password.lower():
            no_consecutive = False
            score -= 5

    checks = [upper, lower, digit, symbol, no_consecutive]
    return score, checks


def generate_password():
    length = random.randint(8, 12)
    password = ''.join(random.sample(symbols, length))
    score = score_calculator(password)
    return password, score[0]


def gen_main(password):
    def regenerate_onClick():
        gen_fr1.forget()
        gen_fr2.forget()
        password, score = generate_password()
        while score <= 25:
            password, score = generate_password()
        gen_main(password)

    def back_to_main_menu_onClick():
        gen_fr1.forget()
        gen_fr2.forget()
        main_menu()

    gen_fr1 = customtkinter.CTkFrame(master=app)
    gen_fr1.pack(pady=10, padx=10, fill="both", expand=True)

    title1_lab = customtkinter.CTkLabel(
        master=gen_fr1, text="Password Generator", font=customtkinter.CTkFont(size=30, weight="bold"), )
    title1_lab.pack(pady=30, padx=10)

    password_lab = customtkinter.CTkLabel(
        master=gen_fr1, text=password, font=customtkinter.CTkFont(size=20, weight="bold"))
    password_lab.pack(pady=10, padx=10)

    gen_fr2 = customtkinter.CTkFrame(master=gen_fr1)
    gen_fr2.pack(pady=20, padx=10, fill="both", expand=True)

    score, checks = score_calculator(password)
    i = 0
    for check in checks:
        if check == True:
            check_txt = customtkinter.CTkTextbox(master=gen_fr2, font=customtkinter.CTkFont(
                size=15), text_color="green", activate_scrollbars=False, height=30, width=300, border_spacing=5)
            check_txt.insert("0.0", names[i])
            check_txt.insert("0.10", "✅             ")
            check_txt.pack(pady=10, padx=5)
        else:
            check_txt = customtkinter.CTkTextbox(master=gen_fr2, font=customtkinter.CTkFont(
                size=15), text_color="red", activate_scrollbars=False, height=30, width=300, border_spacing=5)
            check_txt.insert("0.0", names[i])
            check_txt.insert("0.10", "❎             ")
            check_txt.pack(pady=10, padx=5)
        i = i+1

    strength = "strong"
    color = "green"
    bar_val = 1

    strength_bar = customtkinter.CTkProgressBar(
        master=gen_fr2, progress_color=color, width=300)
    strength_bar.set(bar_val)
    strength_bar.pack(pady=10, padx=10)

    score_lab = customtkinter.CTkLabel(
        master=gen_fr2, text="Score: "+str(score), font=customtkinter.CTkFont(size=20, weight="bold"))
    score_lab.pack(pady=10, padx=10)

    strength_lab = customtkinter.CTkLabel(
        master=gen_fr2, text="Strength: "+strength, font=customtkinter.CTkFont(size=20, weight="bold"))
    strength_lab.pack(pady=15, padx=10)

    regenerate_but = customtkinter.CTkButton(master=gen_fr2, command=regenerate_onClick, text="Re-generate password",
                                             font=customtkinter.CTkFont(size=20), height=40, hover_color=("gray70", "gray30"), width=200)
    regenerate_but.pack(pady=10, padx=10)

    back_to_main_menu_but = customtkinter.CTkButton(master=gen_fr2, command=back_to_main_menu_onClick, text="Main menu", font=customtkinter.CTkFont(
        size=20), height=40, hover_color=("gray70", "gray30"), width=200)
    back_to_main_menu_but.pack(pady=10, padx=10)


main_menu()
app.mainloop()