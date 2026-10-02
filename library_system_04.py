import tkinter as tk
from tkinter import messagebox, ttk
import mysql.connector

# 1. الاتصال بقاعدة البيانات MySQL
db_conn = mysql.connector.connect(
    host="localhost", user="root", password=""  # الباسورد فارغ كما اتفقنا
)
cursor = db_conn.cursor()

# إنشاء القاعدة والجداول إذا لم تكن موجودة
cursor.execute("CREATE DATABASE IF NOT EXISTS library_db")
cursor.execute("USE library_db")
cursor.execute(
    """
    CREATE TABLE IF NOT EXISTS books (
        book_id INT PRIMARY KEY,
        title VARCHAR(100),
        author VARCHAR(100),
        price FLOAT
    )
"""
)
db_conn.commit()


# 2. واجهة إدخال بيانات الكتاب (Add Book Window)
def open_add_window():
  add_win = tk.Toplevel(root)
  add_win.title("Add Book Information")
  add_win.geometry("300x300")

  tk.Label(add_win, text="Book ID:").pack(pady=5)
  e_id = tk.Entry(add_win)
  e_id.pack(pady=5)

  tk.Label(add_win, text="Title:").pack(pady=5)
  e_title = tk.Entry(add_win)
  e_title.pack(pady=5)

  tk.Label(add_win, text="Author:").pack(pady=5)
  e_author = tk.Entry(add_win)
  e_author.pack(pady=5)

  tk.Label(add_win, text="Price:").pack(pady=5)
  e_price = tk.Entry(add_win)
  e_price.pack(pady=5)

  def save_book():
    try:
      b_id = int(e_id.get())
      title = e_title.get()
      author = e_author.get()
      price = float(e_price.get())

      sql = "INSERT INTO books (book_id, title, author, price) VALUES (%s, %s, %s, %s)"
      cursor.execute(sql, (b_id, title, author, price))
      db_conn.commit()

      # Message confirmation dialogs المطلوب
      messagebox.showinfo(
          "Success", "Book added successfully!", parent=add_win
      )
      add_win.destroy()
    except Exception as err:
      messagebox.showerror(
          "Error", f"Failed to add book:\n{err}", parent=add_win
      )

  tk.Button(
      add_win, text="Save Book", bg="green", fg="white", command=save_book
  ).pack(pady=15)


# 3. واجهة عرض السجلات (Display Records Window)
def display_books():
  disp_win = tk.Toplevel(root)
  disp_win.title("Display Records")
  disp_win.geometry("450x300")

  tree = ttk.Treeview(
      disp_win, columns=("ID", "Title", "Author", "Price"), show="headings"
  )
  tree.heading("ID", text="Book ID")
  tree.heading("Title", text="Title")
  tree.heading("Author", text="Author")
  tree.heading("Price", text="Price")
  tree.pack(fill=tk.BOTH, expand=True)

  cursor.execute("SELECT * FROM books")
  for row in cursor.fetchall():
    tree.insert("", tk.END, values=row)


# 4. واجهة البحث عن كتاب (Search Functionality Window)
def search_book():
  search_win = tk.Toplevel(root)
  search_win.title("Search Functionality")
  search_win.geometry("400x350")

  tk.Label(search_win, text="Enter Book Title or ID to Search:").pack(pady=5)
  e_search = tk.Entry(search_win, width=30)
  e_search.pack(pady=5)

  result_box = tk.Text(search_win, height=10, width=45)
  result_box.pack(pady=10)

  def perform_search():
    keyword = e_search.get()
    result_box.delete("1.0", tk.END)

    sql = (
        "SELECT * FROM books WHERE title LIKE %s OR book_id = %s"
        # noqa: E501
    )
    cursor.execute(sql, (f"%{keyword}%", keyword if keyword.isdigit() else 0))
    rows = cursor.fetchall()

    if rows:
      for r in rows:
        result_box.insert(
            tk.END,
            f"ID: {r[0]} | Title: {r[1]} | Author: {r[2]} | Price: {r[3]}\n",
        )
    else:
      result_box.insert(tk.END, "No books found matching your search.")

  tk.Button(search_win, text="Search", command=perform_search).pack(pady=5)


# 5. الواجهة الرئيسية (Desktop Library Manager)
root = tk.Tk()
root.title("Desktop Library Manager - MP-04")
root.geometry("400x350")

tk.Label(
    root, text="Desktop Library Manager", font=("Arial", 14, "bold")
).pack(pady=15)

tk.Button(
    root,
    text="Add Book Information",
    width=25,
    bg="lightblue",
    command=open_add_window,
).pack(pady=8)
tk.Button(
    root,
    text="Display Records",
    width=25,
    bg="lightgreen",
    command=display_books,
).pack(pady=8)
tk.Button(
    root,
    text="Search Functionality",
    width=25,
    bg="lightyellow",
    command=search_book,
).pack(pady=8)
tk.Button(
    root, text="Exit", width=25, bg="salmon", command=root.quit
).pack(pady=8)

root.mainloop()