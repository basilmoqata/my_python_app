import mysql.connector

# 1. الاتصال المبدئي بسيرفر الـ MySQL بدون تحديد قاعدة البيانات
db_conn = mysql.connector.connect(
    host="localhost",
    user="root",          # غيره إذا كان اسم المستخدم عندك مختلف
    password="your_password" # اكتب كلمة المرور الخاصة بقاعدة البيانات عندك
)
cursor = db_conn.cursor()

# 2. إنشاء قاعدة البيانات والجدول تلقائياً
cursor.execute("CREATE DATABASE IF NOT EXISTS library_db")
cursor.execute("USE library_db")
cursor.execute("""
    CREATE TABLE IF NOT EXISTS books (
        book_id INT PRIMARY KEY,
        title VARCHAR(100),
        author VARCHAR(100),
        price FLOAT
    )
""")
print("✅ Database and Table are ready!")

# 3. وظائف النظام (Add, Display, Search, Update, Delete)
def add_book():
    b_id = int(input("Enter Book ID: "))
    title = input("Enter Book Title: ")
    author = input("Enter Author Name: ")
    price = float(input("Enter Price: "))
    
    sql = "INSERT INTO books (book_id, title, author, price) VALUES (%s, %s, %s, %s)"
    val = (b_id, title, author, price)
    cursor.execute(sql, val)
    db_conn.commit()
    print("✅ Book added successfully!\n")

def display_books():
    cursor.execute("SELECT * FROM books")
    result = cursor.fetchall()
    print("\n--- Library Books Records ---")
    for row in result:
        print(f"ID: {row[0]} | Title: {row[1]} | Author: {row[2]} | Price: {row[3]}")
    print("-" * 30 + "\n")

def search_book():
    b_id = int(input("Enter Book ID to search: "))
    cursor.execute("SELECT * FROM books WHERE book_id = %s", (b_id,))
    row = cursor.fetchone()
    if row:
        print(f"🔍 Found: ID: {row[0]} | Title: {row[1]} | Author: {row[2]} | Price: {row[3]}\n")
    else:
        print("❌ Book not found!\n")

def update_book():
    b_id = int(input("Enter Book ID to update: "))
    new_price = float(input("Enter new price: "))
    cursor.execute("UPDATE books SET price = %s WHERE book_id = %s", (new_price, b_id))
    db_conn.commit()
    print("✅ Book updated successfully!\n")

def delete_book():
    b_id = int(input("Enter Book ID to delete: "))
    cursor.execute("DELETE FROM books WHERE book_id = %s", (b_id,))
    db_conn.commit()
    print("🗑️ Book deleted successfully!\n")

# 4. القائمة الرئيسية للنظام (Menu Loop)
while True:
    print("=== Library Management System ===")
    print("1. Add Book")
    print("2. Display All Books")
    print("3. Search Book")
    print("4. Update Book Price")
    print("5. Delete Book")
    print("6. Exit")
    
    choice = input("Choose an option (1-6): ")
    
    if choice == '1':
        add_book()
    elif choice == '2':
        display_books()
    elif choice == '3':
        search_book()
    elif choice == '4':
        update_book()
    elif choice == '5':
        delete_book()
    elif choice == '6':
        print("Exiting system. Goodbye!")
        break
    else:
        print("❌ Invalid choice, please try again.\n")