from flask import Flask, redirect, render_template_string, request, url_for
import mysql.connector

app = Flask(__name__)

# الاتصال بقاعدة البيانات MySQL
db_config = {
    "host": "localhost",
    "user": "root",
    "password": "",
    "database": "library_db",
}


def get_db_connection():
  conn = mysql.connector.connect(**db_config)
  return conn


# إنشاء الجدول إذا لم يكن موجوداً
conn = mysql.connector.connect(
    host="localhost", user="root", password=""
)
cursor = conn.cursor()
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
conn.commit()
cursor.close()
conn.close()

# قالب HTML مدمج لتسهيل التشغيل بدون الحاجة لمجلد templates خارجي
TEMPLATE = """
<!doctype html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Dynamic Library Website - MP-05</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 40px; background-color: #f4f4f9; color: #333; }
        h1, h2 { color: #2c3e50; }
        nav a { margin-right: 15px; text-decoration: none; color: #3498db; font-weight: bold; }
        table { width: 100%; border-collapse: collapse; margin-top: 20px; background: white; }
        th, td { border: 1px solid #ddd; padding: 10px; text-align: left; }
        th { background-color: #3498db; color: white; }
        form { background: white; padding: 20px; border-radius: 5px; width: 300px; box-shadow: 0 0 10px rgba(0,0,0,0.1); }
        input { width: 100%; padding: 8px; margin: 5px 0 15px 0; border: 1px solid #ccc; border-radius: 4px; }
        button { background: #2ecc71; color: white; border: none; padding: 10px 15px; border-radius: 4px; cursor: pointer; }
        button:hover { background: #27ae60; }
    </style>
</head>
<body>
    <h1>Dynamic Library Website (MP-05)</h1>
    <nav>
        <a href="{{ url_for('index') }}">Home</a>
        <a href="{{ url_for('add_book') }}">Add Book</a>
        <a href="{{ url_for('search_book') }}">Search Books</a>
    </nav>
    <hr>

    {% if page == 'home' %}
        <h2>Welcome to the Library Homepage</h2>
        <p>Use the navigation links above to manage your books dynamically using Flask and MySQL.</p>

    {% elif page == 'add' %}
        <h2>Add Book Form</h2>
        <form method="POST">
            <label>Book ID:</label>
            <input type="number" name="book_id" required>
            <label>Title:</label>
            <input type="text" name="title" required>
            <label>Author:</label>
            <input type="text" name="author" required>
            <label>Price:</label>
            <input type="number" step="0.01" name="price" required>
            <button type="submit">Save Book</button>
        </form>

    {% elif page == 'display' %}
        <h2>Display Books List</h2>
        <table>
            <tr>
                <th>Book ID</th>
                <th>Title</th>
                <th>Author</th>
                <th>Price</th>
            </tr>
            {% for book in books %}
            <tr>
                <td>{{ book[0] }}</td>
                <td>{{ book[1] }}</td>
                <td>{{ book[2] }}</td>
                <td>{{ book[3] }}</td>
            </tr>
            {% else %}
            <tr><td colspan="4">No books found in the database.</td></tr>
            {% endfor %}
        </table>

    {% elif page == 'search' %}
        <h2>Search Functionality</h2>
        <form method="GET" style="margin-bottom: 20px;">
            <label>Search by Title or ID:</label>
            <input type="text" name="q" value="{{ query }}">
            <button type="submit" style="background: #3498db;">Search</button>
        </form>
        {% if results is not none %}
            <h3>Results:</h3>
            <table>
                <tr>
                    <th>Book ID</th>
                    <th>Title</th>
                    <th>Author</th>
                    <th>Price</th>
                </tr>
                {% for book in results %}
                <tr>
                    <td>{{ book[0] }}</td>
                    <td>{{ book[1] }}</td>
                    <td>{{ book[2] }}</td>
                    <td>{{ book[3] }}</td>
                </tr>
                {% else %}
                <tr><td colspan="4">No matching books found.</td></tr>
                {% endfor %}
            </table>
        {% endif %}
    {% endif %}
</body>
</html>
"""


@app.route("/")
def index():
  conn = get_db_connection()
  cursor = conn.cursor()
  cursor.execute("SELECT * FROM books")
  books = cursor.fetchall()
  cursor.close()
  conn.close()
  return render_template_string(TEMPLATE, page="display", books=books)


@app.route("/add", methods=["GET", "POST"])
def add_book():
  if request.method == "POST":
    b_id = request.form["book_id"]
    title = request.form["title"]
    author = request.form["author"]
    price = request.form["price"]

    conn = get_db_connection()
    cursor = conn.cursor()
    try:
      cursor.execute(
          "INSERT INTO books (book_id, title, author, price) VALUES (%s,"
          " %s, %s, %s)",
          (b_id, title, author, price),
      )
      conn.commit()
    except Exception as e:
      print("Error:", e)
    finally:
      cursor.close()
      conn.close()
    return redirect(url_for("index"))
  return render_template_string(TEMPLATE, page="add")


@app.route("/search")
def search_book():
  query = request.args.get("q", "")
  results = None
  if query:
    conn = get_db_connection()
    cursor = conn.cursor()
    sql = "SELECT * FROM books WHERE title LIKE %s OR book_id = %s"
    cursor.execute(sql, (f"%{query}%", query if query.isdigit() else 0))
    results = cursor.fetchall()
    cursor.close()
    conn.close()
  return render_template_string(TEMPLATE, page="search", results=results, query=query)


if __name__ == "__main__":
  app.run(debug=True)