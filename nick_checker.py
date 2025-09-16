import requests
import tkinter as tk
from urls import urls
from threading import Thread
from tkinter import scrolledtext, messagebox, ttk


def check_user_exists(username, output_box, progress_bar, search_button):
    exists = [
        f"Список социальных сетей {username}",
        "-" * 60,
    ]

    total = len(urls)
    progress_bar["maximum"] = total
    progress_bar["value"] = 0
    search_button.config(state=tk.DISABLED)

    for i, url in enumerate(urls, 1):
        user_url = url + username
        try:
            response = requests.get(
                user_url, allow_redirects=True, timeout=5)
            if response.status_code == 200:
                exists.append(user_url)
        except Exception as e:
            print(f"Ошибка: {e}")

        progress_bar["value"] = i
        progress_bar.update_idletasks()

    result = "\n".join(exists)

    output_box.delete(1.0, tk.END)
    output_box.insert(tk.END, result)

    with open(f"{username}.txt", 'w', encoding="utf-8") as f:
        f.write(result)

    search_button.config(
        state=tk.NORMAL
        )


def start_search(
    entry, 
    output_box, 
    progress_bar, 
    search_button
    ):
    username = entry.get().strip()
    if not username:
        messagebox.showwarning(
            "Ошибка", 
            "Введите имя пользователя!"
            )
        return
    
    thread = Thread(
        target=check_user_exists, 
        args=(
            username, 
            output_box, 
            progress_bar, 
            search_button
            )
        )
    thread.start()


def main():
    root = tk.Tk()
    root.title("Поиск пользователя по никнейму")
    root.geometry("600x450")

    tk.Label(
        root, 
        text="Введите имя пользователя:"
        ).pack(pady=5)
    entry = tk.Entry(
        root, 
        width=40
        )
    entry.pack(
        pady=5
        )

    output_box = scrolledtext.ScrolledText(
        root, 
        wrap=tk.WORD, 
        width=70, 
        height=15
        )
    output_box.pack(
        pady=10
        )

    progress_bar = ttk.Progressbar(
        root, 
        orient="horizontal", 
        length=500, 
        mode="determinate"
        )
    progress_bar.pack(
        pady=5
        )

    search_button = tk.Button(
        root, 
        text="Поиск", 
        command=lambda: start_search(
            entry, 
            output_box, 
            progress_bar, 
            search_button
            )
    )
    search_button.pack(pady=5)

    root.mainloop()


if __name__ == "__main__":
    main()
