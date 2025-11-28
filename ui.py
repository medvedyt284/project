import tkinter as tk
from tkinter import ttk, messagebox
from database import Database


class BookApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Book Database")

        self.db = Database("books.db")

        self.create_widgets()
        self.load_books()

    def create_widgets(self):
        # Поле для поиска
        self.search_label = tk.Label(self.root, text="Введите текст")
        self.search_label.pack()

        self.search_entry = tk.Entry(self.root)
        self.search_entry.pack()
        # Кнопка поиска
        self.search_button = tk.Button(self.root, text="Найти", command=self.search_books)
        self.search_button.pack()

        # Кнопка для добавления книги
        self.add_button = tk.Button(self.root, text="Добавить Книгу", command=self.open_add_book_window)
        self.add_button.pack()

        # Таблица для отображения книг
        self.table = ttk.Treeview(self.root, columns=("ID", "Название", "Автор", "Год"), show='headings')
        self.table.heading("ID", text="ID")
        self.table.heading("Название", text="Название")
        self.table.heading("Автор", text="Автор")
        self.table.heading("Год", text="Год")
        self.table.pack()

    def load_books(self):
        for item in self.table.get_children():
            self.table.delete(item)

        for book in self.db.get_all_books():
            self.table.insert('', 'end', values=book)

    def search_books(self):
        query = self.search_entry.get()
        results = self.db.search_books(query)

        for item in self.table.get_children():
            self.table.delete(item)

        for book in results:
            self.table.insert('', 'end', values=book)
    # Добавление книги
    def open_add_book_window(self):
        add_window = tk.Toplevel(self.root)
        add_window.title("Add Book")

        tk.Label(add_window, text="Название:").pack()
        title_entry = tk.Entry(add_window)
        title_entry.pack()

        tk.Label(add_window, text="Автор:").pack()
        author_entry = tk.Entry(add_window)
        author_entry.pack()

        tk.Label(add_window, text="Год:").pack()
        year_entry = tk.Entry(add_window)
        year_entry.pack()

        add_button = tk.Button(add_window, text="Добавить",
                               command=lambda: self.add_book(title_entry.get(), author_entry.get(), year_entry.get(),
                                                             add_window))
        add_button.pack()

    def add_book(self, title, author, year, window):
        if title and author and year.isdigit():
            self.db.add_book(title, author, int(year))
            messagebox.showinfo("Success", "Книга успешно добавлена!")
            window.destroy()
            self.load_books()
        else:
            messagebox.showerror("Error", "Пожалуйста введите правильное значение.")

    def close(self):
        self.db.close()


if __name__ == "__main__":
    root = tk.Tk()
    app = BookApp(root)
    root.protocol("WM_DELETE_WINDOW", app.close)
    root.mainloop()
