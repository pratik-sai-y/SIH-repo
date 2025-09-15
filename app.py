from flask import Flask, render_template, request, redirect, url_for, session

app = Flask(__name__)
app.secret_key = "secretkey123"   # needed for sessions

# Fake user database (for demo)
users = {}

# Quiz data
quiz = [
    {"q": "What is the capital of India?", "a": "New Delhi"},
    {"q": "Which planet is known as the Red Planet?", "a": "Mars"},
    {"q": "What is 15 + 6?", "a": "21"},
    {"q": "Who is known as the Father of Computers?", "a": "Charles Babbage"},
    {"q": "What is the chemical symbol for water?", "a": "H2O"}
]

# Home page
@app.route('/')
@app.route('/home')
def home():
    return render_template("home.html")
# Registration
@app.route('/register', methods=["GET", "POST"])
def registration():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        if username in users:
            return "⚠️ Username already exists!"
        users[username] = password
        return redirect(url_for("login"))

    return render_template("registration.html")

# Login
@app.route('/login', methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        if username in users and users[username] == password:
            session["user"] = username
            return redirect(url_for("homepage"))
        else:
            return "❌ Invalid username or password!"

    return render_template("login.html")

# Logout
@app.route('/logout')
def logout():
    session.pop("user", None)
    return redirect(url_for("login"))
@app.route('/homepage')
def homepage():
    return render_template('homepage.html')

# Quiz
@app.route('/lvl')
def lvl():
    return render_template('lvl.html')
@app.route('/quiz', methods=["GET", "POST"])
def quiz_page():
    if "user" not in session:
        return redirect(url_for("login"))

    if "index" not in session:
        session["index"] = 0
        session["score"] = 0

    if request.method == "POST":
        user_ans = request.form.get("answer", "")
        correct_ans = quiz[session["index"]]["a"]

        if user_ans.strip().lower() == correct_ans.strip().lower():
            session["score"] += 1

        session["index"] += 1

    if session["index"] >= len(quiz):  # quiz finished
        score = session["score"]
        session.pop("index", None)
        session.pop("score", None)
        return render_template("result.html", score=score, total=len(quiz))

    return render_template("quiz.html",
                           question=quiz[session["index"]]["q"],
                           index=session["index"]+1,
                           total=len(quiz))

if __name__ == "__main__":
    app.run(debug=True)
