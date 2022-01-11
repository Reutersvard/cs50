import os
from cs50 import SQL
from flask import Flask, flash, jsonify, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import apology, login_required, lookup, usd

# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Ensure responses aren't cached


@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


# Custom filter
app.jinja_env.filters["usd"] = usd

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///finance.db")

# Make sure API key is set
if not os.environ.get("API_KEY"):
    raise RuntimeError("API_KEY not set")


@app.route("/", methods=["GET", "POST"])
@login_required
def index():
    """Show portfolio of stocks"""

    if request.method == "GET":

        # Returns a list of dicts e.g. [{'symbol': 'AAPL', 'shares': 3}, {'symbol': 'TOM', 'shares': 1}]
        portfolio = db.execute(
            "SELECT symbol, SUM (shares) AS shares FROM portfolio WHERE user_id = :user_id GROUP BY symbol", user_id=session["user_id"])

        # Returns a value e.g. 10000
        cash = db.execute("SELECT cash FROM users WHERE id = :user_id", user_id=session["user_id"])[0]["cash"]

        # Create lists to perform operations on
        names = []
        shares_price = []
        shares_amount = []

        for row in portfolio:

            if row["shares"] != 0:
                dict_ = lookup(row["symbol"])
                names.append(dict_["name"])
                shares_price.append(dict_["price"])
                shares_amount.append(row["shares"])

        shares_holding = [a * b for a, b in zip(shares_price, shares_amount)]
        total_shares = sum(shares_holding)
        total_cash = cash + total_shares

        return render_template("index.html", portfolio=portfolio, names=names, shares_price=shares_price,
                               shares_holding=shares_holding, cash=cash, total_cash=total_cash)
    else:

        cash = db.execute("SELECT cash FROM users WHERE id = :user_id", user_id=session["user_id"])[0]["cash"]
        balance = cash + 10000
        db.execute("UPDATE users SET cash = :cash WHERE id = :user_id", cash=balance, user_id=session["user_id"])

        return redirect("/")


@app.route("/buy", methods=["GET", "POST"])
@login_required
def buy():
    """Buy shares of stock"""
    if request.method == "POST":

        if not request.form.get("symbol"):
            return apology("missing symbol", 400)

        if not request.form.get("shares"):
            return apology("missing amount of shares", 400)

        if not request.form.get("shares").isdigit():
            return apology("amount of shares must be a positive integer", 400)

        quote = lookup(request.form.get("symbol"))

        if quote is None:
            return apology("could not retreive stock's symbol", 400)

        shares = int(request.form.get("shares"))
        price = quote["price"]
        cash = db.execute("SELECT cash FROM users WHERE id = :user_id", user_id=session["user_id"])[0]["cash"]

        balance = cash - price * shares

        if balance < 0:
            return apology("not enough cash available", 400)

        db.execute("INSERT INTO portfolio (user_id, symbol, shares, price) VALUES (:user_id, :symbol, :shares, :price)",
                   user_id=session["user_id"], symbol=quote["symbol"], shares=shares, price=price)

        db.execute("UPDATE users SET cash = :cash WHERE id = :user_id", cash=balance, user_id=session["user_id"])

        return redirect("/")

    else:
        return render_template("buy.html")


@app.route("/history")
@login_required
def history():
    """Show history of transactions"""

    # Returns a list of dicts e.g. [{'symbol': 'AAPL', 'shares': 3}, {'symbol': 'TOM', 'shares': 1}]
    portfolio = db.execute("SELECT symbol, shares, price, timestamp FROM portfolio WHERE user_id = :user_id",
                           user_id=session["user_id"])

    return render_template("history.html", portfolio=portfolio)


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 403)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 403)

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = :username",
                          username=request.form.get("username"))

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return apology("invalid username and/or password", 403)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")


@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")


@app.route("/quote", methods=["GET", "POST"])
@login_required
def quote():
    """Get stock quote."""

    if request.method == "POST":

        quote = lookup(request.form.get("symbol"))

        if quote is None:
            return apology("could not retreive quote", 400)
        else:
            return render_template("quoted.html", Company_Name=quote["name"], Latest_Price=quote["price"], Symbol=quote["symbol"])

    else:
        return render_template("quote.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""
    if request.method == "POST":

        # Query database for username and ensure username does not exist already
        namelist = db.execute("SELECT username FROM users WHERE username = :username", username=request.form.get("username"))
        if len(namelist) > 0:
            return apology("username already exists", 400)

        # Ensure username was submitted
        elif not request.form.get("username"):
            return apology("must provide username", 400)

        # Ensure password was submitted and matches confirmation
        elif not request.form.get("password"):
            return apology("must provide password", 400)

        elif request.form.get("password") != request.form.get("confirmation"):
            return apology("passwords do not match", 400)

        # Hash password and query database for username
        h_password = generate_password_hash(request.form.get("password"))
        db.execute("INSERT INTO users (username, hash) VALUES (:username, :hash_)",
                   username=request.form.get("username"), hash_=h_password)

        return render_template("registered.html")

    else:
        return render_template("register.html")


@app.route("/sell", methods=["GET", "POST"])
@login_required
def sell():
    """Sell shares of stock"""

    # Returns a list of dicts e.g. [{'symbol': 'AAPL', 'shares': 3}, {'symbol': 'TOM', 'shares': 1}]
    portfolio = db.execute(
        "SELECT symbol, SUM (shares) AS shares FROM portfolio WHERE user_id = :user_id GROUP BY symbol", user_id=session["user_id"])

    # Create a list for the user's available stocks, and a dict with them and their amounts
    owned_amounts = {}
    symbols = []
    for row in portfolio:
        if row["shares"] != 0:
            symbols.append(row["symbol"])
            owned_amounts[row["symbol"]] = row["shares"]

    if request.method == "POST":

        # Getting the current price of shares, the amount requested to be sold, and the user's current cash balance

        if not request.form.get("symbol"):
            return apology("missing symbol", 400)

        if not request.form.get("shares"):
            return apology("missing amount of shares", 400)

        quote = lookup(request.form.get("symbol"))

        price = quote["price"]
        shares = int(request.form.get("shares"))
        cash = db.execute("SELECT cash FROM users WHERE id = :user_id", user_id=session["user_id"])[0]["cash"]

        if shares < 1:
            return apology("amount of shares must be a positive integer", 400)

        elif owned_amounts[request.form.get("symbol")] < shares:
            return apology("not enough shares to sell", 400)

        else:

            balance = cash + (price * shares)
            db.execute("UPDATE users SET cash=:cash WHERE id = :user_id", cash=balance, user_id=session["user_id"])
            db.execute("INSERT INTO portfolio (user_id, symbol, shares, price) VALUES (:user_id, :symbol, :shares, :price)",
                       user_id=session["user_id"], symbol=quote["symbol"], shares=-shares, price=price)

            return redirect("/")

    else:
        return render_template("sell.html", symbols=symbols)


def errorhandler(e):
    """Handle error"""
    if not isinstance(e, HTTPException):
        e = InternalServerError()
    return apology(e.name, e.code)


# Listen for errors
for code in default_exceptions:
    app.errorhandler(code)(errorhandler)
