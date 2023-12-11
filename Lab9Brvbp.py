import os
from tkinter import *
from tkinter import messagebox
from tkinter import ttk


def open_file():
    try:
        text = open(r"authorization_file.txt", "r+")
        return text
    except FileNotFoundError:
        text = open(r"authorization_file.txt", "w")
        text.close()
        text = open(r"authorization_file.txt", "r+")
        return text


def dismiss(windows):
    windows.grab_release()
    windows.destroy()


class StartWindow:
    def __init__(self, main):
        self.main = main
        self.accounts = {}

        style_text = ttk.Style()
        style_text.configure("my.TButton", font="Arial 9")

        self.login = ttk.Entry(width=20)
        self.password = ttk.Entry(width=20)

        self.login.place(x=200, y=70)
        self.password.place(x=200, y=100)

        Label(text="Добро пожаловать, введите свой логин и пароль", font="Arial 10").place(x=100, y=20)
        Label(text="Логин", font="Arial 10").place(x=150, y=70)
        Label(text="Пароль", font="Arial 10").place(x=142, y=100)
        ttk.Button(text="Авторизация", width=17, style="my.TButton", command=lambda: self.authorization()).place(x=200, y=130)
        ttk.Button(text="Регистрация", width=17, style="my.TButton", command=lambda: self.registration()).place(x=200, y=160)

    def authorization(self):
        login = self.login.get()
        password = self.password.get()

        if len(login) == 0 or len(password) == 0:
            messagebox.showwarning(title="Ошибка", message="Поле заполнения пусто")

        else:
            file = open_file()
            a = file.readline()[:-1].split(" ")

            while True:
                if a != [""]:
                    self.accounts[a[0]] = a[1]
                    a = file.readline()[:-1].split(" ")
                else:
                    break

            flag_reg = False
            flag_password = True
            for i in self.accounts.items():
                l, p = i
                if login == l and password == p:
                    flag_reg = True
                    break
                elif login == l and password != p:
                    flag_password = False

            if flag_reg:
                for widget in self.main.winfo_children():
                    widget.destroy()

                Label(self.main, text="Вы успешно авторизовались!", font="Arial 12 bold").place(x=120, y=80)
                ttk.Button(self.main, text="Играть", style="my.TButton", command=lambda: self.drawing()).place(x=200, y=150)

            elif not flag_password:
                messagebox.showwarning(title="Ошибка", message="Неверный пароль")
            else:
                messagebox.showwarning(title="Ошибка", message="Такого аккаунта не существует")

    def registration(self):
        window = Toplevel()
        window.geometry("480x320+100+100")
        window.title("Регистрация")
        window.resizable(False, False)
        window.protocol("WM_DELETE_WINDOW", lambda: dismiss(window))
        window.grab_set()

        login_reg = ttk.Entry(window, width=20)
        password_reg = ttk.Entry(window, width=20)

        login_reg.place(x=200, y=70)
        password_reg.place(x=200, y=100)

        Label(window, text="Введите желаемый логин и пароль", font="Arial 10").place(x=100, y=20)
        Label(window, text="Логин", font="Arial 10").place(x=150, y=70)
        Label(window, text="Пароль", font="Arial 10").place(x=142, y=100)
        ttk.Button(window, text="Регистрация", width=17, style="my.TButton", command=lambda: registrate()).place(x=200, y=130)

        def registrate():
            login = login_reg.get()
            password = password_reg.get()

            if len(login) == 0 or len(password) == 0:
                messagebox.showwarning(title="Ошибка", message="Поле заполнения пусто")
            else:
                file = open_file()
                a = file.readline()[:-1].split(" ")

                while True:
                    if a != ['']:
                        self.accounts[a[0]] = a[1]
                        a = file.readline()[:-1].split(" ")
                    else:
                        break

                flag_reg = False

                for i in self.accounts.items():
                    log, pasw = i
                    if login == log:
                        flag_reg = True

                if not flag_reg:
                    file = open_file()
                    file.seek(0, os.SEEK_END)
                    file.write(f'{login} {password}\n')
                    file.close()

                    for h in window.winfo_children():
                        h.destroy()

                    Label(window, text="Вы успешно зарегистрировались", font="Arial 10 bold").place(x=120, y=80)
                    window.after(2000, lambda: (window.destroy(), window.grab_release()))
                else:
                    messagebox.showwarning(title="Ошибка", message="Такой аккаунт уже существует")

    def drawing(self):
        self.main.geometry('560x560+560+100')
        self.main.title("Шашки")

        rows = cols = 8
        size = 70

        deck = Canvas(self.main, width=size * rows, height=size * cols)

        cell_colors = ["#E5E5E5", "#663300"]
        color_index = 0

        for row in range(rows):
            for col in range(cols):
                x1, y1 = col * size, row * size
                x2, y2 = col * size + size, row * size + size
                deck.create_rectangle((x1, y1), (x2, y2), fill=cell_colors[color_index])

                color_index = not color_index

            color_index = not color_index

        deck.pack()


root = Tk()
root.title("Авторизация")
root.geometry("480x320+100+100")
root.resizable(False, False)

StartWindow(root)

root.mainloop()
