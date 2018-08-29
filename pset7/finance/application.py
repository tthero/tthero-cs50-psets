import os

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import apology, login_required, lookup, usd

# Ensure environment variable is set
if not os.environ.get("API_KEY"):
    raise RuntimeError("API_KEY not set")

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


@app.route("/", methods=["GET", "POST"])
@login_required
def index():
    """Show portfolio of stocks"""

    t_id = "table_id" + str(session["user_id"])

    if request.method == "GET":
        # Use render_template? Along with a list of data retrieved from finance.db?
        """
        Stock   Name    Number of shares    Current price   TOTAL   |   Buy/Sell
        GOOG    GOOG            1               $333        $333    |
        CASH                                                $9667   |
        """

        temp = db.execute("SELECT stock FROM :table_id GROUP BY stock HAVING SUM(shareflow) > 0",
                          table_id=t_id)
        for i in range(len(temp)):
            info = lookup(temp[i]["stock"])
            if info is not None:
                db.execute("UPDATE :table_id SET cur_price = :price WHERE stock = :stock",
                           table_id=t_id, price=info["price"], stock=info["symbol"])

        items = db.execute("SELECT stock, SUM(shareflow) AS share_sum, cur_price, \
                            SUM(shareflow) * cur_price AS total_price \
                            FROM :table_id GROUP BY stock HAVING share_sum > 0", table_id=t_id)
        cash = db.execute("SELECT cash FROM users WHERE id = :uid",
                          uid=session["user_id"])

        # To calculate grand total
        g_total = 0
        for item in items:
            g_total += item["total_price"]
        g_total += cash[0]["cash"]

        return render_template("index.html", items=items, c_left=cash, total=g_total)
    else:
        # BUY section
        if 'buyer' in request.form:
            if not request.form.get("buy_stock") or not request.form.get("buy_shares"):
                flash("Invalid buying input!", 'error')
                return redirect("/")
            else:
                try:
                    if int(request.form.get("buy_shares")) <= 0:
                        flash("Invalid buying input!", 'error')
                        return redirect("/")
                except ValueError:
                    flash("Invalid buying input!", 'error')
                    return redirect("/")

            info = lookup(request.form.get("buy_stock"))

            if info is None:
                flash("Symbol info is unavailable! Try again later!", 'error')
                return redirect("/")
            else:
                # Fetch the cash
                cash = db.execute("SELECT cash FROM users WHERE id = :uid", uid=session["user_id"])

                # If cash < share * price, not enough
                if cash[0]["cash"] < float(request.form.get("buy_shares")) * info["price"]:
                    flash("Not enough cash!", 'error')
                    return redirect("/")
                else:
                    # Add new transaction data
                    # Consists of stock, share flow, price and transaction datetime
                    db.execute("INSERT INTO :table_id ('stock', 'shareflow', 'cur_price',\
                               'trn_price', 'trn_time') VALUES (:stock, :shareflow, :price, \
                               :price, datetime('now', 'localtime'))",
                               table_id=t_id, stock=info["symbol"],
                               shareflow=request.form.get("buy_shares"),
                               price=info["price"])

                    # Update the available cash
                    db.execute("UPDATE users SET cash = :cash WHERE id = :uid",
                               cash=cash[0]["cash"] - float(request.form.get("buy_shares")) * info["price"],
                               uid=session["user_id"])

                    flash("You have successfully bought {0} shares of {1}!".format(
                          request.form.get("buy_shares"), info["symbol"]), 'info')
                    return redirect("/")
        # SELL section
        elif 'seller' in request.form:
            if not request.form.get("sell_stock") or not request.form.get("sell_shares"):
                flash("Invalid selling input!", 'error')
                return redirect("/")
            else:
                try:
                    if int(request.form.get("sell_shares")) <= 0:
                        flash("Invalid selling input!", 'error')
                        return redirect("/")
                except ValueError:
                    flash("Invalid selling input!", 'error')
                    return redirect("/")

            # sh is to check if the stock exists in DATABASE or not
            # info is to check if the stock exists in INTERNET or not
            sh = db.execute("SELECT stock FROM :table_id WHERE stock = :stock",
                            table_id=t_id, stock=request.form.get("sell_stock"))
            info = lookup(request.form.get("sell_stock"))

            if not sh:
                flash("Stock not found!", 'error')
                return redirect("/")
            elif info is None:
                flash("Symbol info is unavailable! Try again later!", 'error')
                return redirect("/")
            else:
                # Fetch the cash
                cash = db.execute("SELECT cash FROM users WHERE id = :uid", uid=session["user_id"])

                # Fetch the number of shares
                share = db.execute("SELECT sum(shareflow) AS share_sum FROM :table_id \
                                   WHERE stock = :stock", table_id=t_id,
                                   stock=request.form.get("sell_stock"))

                if share[0]["share_sum"] < float(request.form.get("sell_shares")):
                    flash("Not enough shares to sell!", 'error')
                    return redirect("/")
                else:
                    # Add new transaction data
                    # Consists of stock, share flow, price and transaction datetime
                    db.execute("INSERT INTO :table_id ('stock', 'shareflow', 'cur_price',\
                               'trn_price', 'trn_time') VALUES (:stock, -:shareflow, :price, \
                               :price, datetime('now', 'localtime'))",
                               table_id=t_id, stock=info["symbol"],
                               shareflow=request.form.get("sell_shares"), price=info["price"])

                    # Update the available cash
                    db.execute("UPDATE users SET cash = :cash WHERE id = :uid",
                               cash=cash[0]["cash"] + float(request.form.get("sell_shares")) * info["price"],
                               uid=session["user_id"])

                    flash("You have successfully sold {0} shares of {1}!".format(
                          request.form.get("sell_shares"), info["symbol"]), 'info')
                    return redirect("/")
        # CASH-IN section
        # Now unable to put transaction of cashing in more money
        # into history, will be done in the future
        elif 'cash_in' in request.form:
            if not request.form.get("cash_in") or not request.form.get("cash_val"):
                flash("Invalid cash input!", 'error')
                return redirect("/")
            else:
                try:
                    if float(request.form.get("cash_val")) <= 0:
                        flash("Invalid cash input!", 'error')
                        return redirect("/")
                except ValueError:
                    flash("Invalid cash input!", 'error')
                    return redirect("/")

            # Fetch the cash
            cash = db.execute("SELECT cash FROM users WHERE id = :uid", uid=session["user_id"])

            # Update the available cash
            db.execute("UPDATE users SET cash = :cash WHERE id = :uid",
                       cash=cash[0]["cash"] + float(request.form.get("cash_val")),
                       uid=session["user_id"])

            flash("You have cashed in ${0:,.2f}!".format(
                  float(request.form.get("cash_val"))), 'info')
            return redirect("/")


@app.route("/quote", methods=["GET", "POST"])
@login_required
def quote():
    """Get stock quote."""

    if request.method == "POST":

        # Search for the symbol and its price
        info = lookup(request.form.get("symbol"))

        # If info is invalid
        if info is None:
            return apology("invalid/no such symbol")
        else:
            return render_template("quoted.html", info=info)
    else:
        return render_template("quote.html")


@app.route("/buy", methods=["GET", "POST"])
@login_required
def buy():
    """Buy shares of stock"""

    if request.method == "POST":
        if not request.form.get("symbol"):
            return apology("must provide symbol")
        elif not request.form.get("shares"):
            return apology("must provide valid number of shares")
        else:
            try:
                if int(request.form.get("shares")) <= 0:
                    return apology("must provide valid number of shares")
            except ValueError:
                return apology("must provide valid number of shares")

        info = lookup(request.form.get("symbol"))

        if info is None:
            return apology("invalid/no such symbol")
        else:
            # Fetch the cash
            cash = db.execute("SELECT cash FROM users WHERE id = :uid", uid=session["user_id"])

            # If cash < share * price, not enough
            if cash[0]["cash"] < float(request.form.get("shares")) * info["price"]:
                return apology("not enough cash")
            else:
                # Add new transaction data
                # Consists of stock, share flow, price and transaction datetime
                db.execute("INSERT INTO :table_id ('stock', 'shareflow', 'cur_price',\
                           'trn_price', 'trn_time') VALUES (:stock, :shareflow, :price, \
                           :price, datetime('now', 'localtime'))",
                           table_id="table_id" + str(session["user_id"]),
                           stock=info["symbol"], shareflow=request.form.get("shares"),
                           price=info["price"])

                # Update the available cash
                db.execute("UPDATE users SET cash = :cash WHERE id = :uid",
                           cash=cash[0]["cash"] - float(request.form.get("shares")) * info["price"],
                           uid=session["user_id"])

                flash("You have successfully bought {0} shares of {1}!".format(
                      request.form.get("shares"), info["symbol"]), 'info')

                return redirect("/")
    else:
        return render_template("buy.html")


@app.route("/sell", methods=["GET", "POST"])
@login_required
def sell():
    """Sell shares of stock"""

    t_id = "table_id" + str(session["user_id"])

    if request.method == "POST":
        if not request.form.get("symbol"):
            return apology("please select stock")
        elif not request.form.get("shares"):
            return apology("must provide valid number of shares")
        else:
            try:
                if int(request.form.get("shares")) <= 0:
                    return apology("must provide valid number of shares")
            except ValueError:
                return apology("must provide valid number of shares")

        # sh is to check if the stock exists in DATABASE or not
        # info is to check if the stock exists in INTERNET or not
        sh = db.execute("SELECT stock FROM :table_id WHERE stock = :stock",
                        table_id=t_id, stock=request.form.get("symbol"))
        info = lookup(request.form.get("symbol"))

        if not sh:
            return apology("you do not have that share")
        elif info is None:
            return apology("invalid/no such symbol")
        else:
            # Fetch the cash
            cash = db.execute("SELECT cash FROM users WHERE id = :uid", uid=session["user_id"])

            # Fetch the number of shares
            share = db.execute("SELECT sum(shareflow) AS share_sum FROM :table_id \
                               WHERE stock = :stock", table_id=t_id,
                               stock=request.form.get("symbol"))

            if share[0]["share_sum"] < float(request.form.get("shares")):
                return apology("not enough shares")
            else:
                # Add new transaction data
                # Consists of stock, share flow, price and transaction datetime
                db.execute("INSERT INTO :table_id ('stock', 'shareflow', 'cur_price',\
                           'trn_price', 'trn_time') VALUES (:stock, -:shareflow, :price, \
                           :price, datetime('now', 'localtime'))",
                           table_id=t_id, stock=info["symbol"],
                           shareflow=request.form.get("shares"), price=info["price"])

                # Update the available cash
                db.execute("UPDATE users SET cash = :cash WHERE id = :uid",
                           cash=cash[0]["cash"] + float(request.form.get("shares")) * info["price"],
                           uid=session["user_id"])

                flash("You have successfully sold {0} shares of {1}!".format(
                      request.form.get("shares"), info["symbol"]), 'info')

                return redirect("/")

    else:
        items = db.execute("SELECT DISTINCT stock FROM :table_id GROUP BY stock \
                           HAVING sum(shareflow) > 0", table_id=t_id)

        return render_template("sell.html", stock=items)


@app.route("/history")
@login_required
def history():
    """Show history of transactions"""

    t_id = "table_id" + str(session["user_id"])

    # Shows stock, share flow, price during transaction, transaction time
    items = db.execute("SELECT stock, shareflow, trn_price, trn_time \
                       FROM :table_id ORDER BY trn_time DESC", table_id=t_id)

    return render_template("history.html", items=items)


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


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""

    if request.method == "POST":
        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username")

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password")

        # Ensure confirmation was also submitted
        elif not request.form.get("confirmation"):
            return apology("re-type your password as well")

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = :username",
                          username=request.form.get("username"))

        # If username exists, password and confirmation are different
        if len(rows) == 1:
            return apology("username already exists")
        elif request.form.get("password") != request.form.get("confirmation"):
            return apology("passwords mismatch")

        # Create new entry for this new user
        user_id = db.execute("INSERT INTO users (username, hash) \
                             VALUES (:username, :pwd_hash)",
                             username=request.form.get("username"),
                             pwd_hash=generate_password_hash(request.form.get("password")))

        # Remember which user has logged in
        session["user_id"] = user_id

        # Shows confirmation message
        flash("Registered!", 'info')

        # Creates new table to store the stock, shares flow, current price,
        # price on time, transaction date
        db.execute("CREATE TABLE IF NOT EXISTS :table_id ( \
                   'trn_id' INTEGER PRIMARY KEY NOT NULL, \
                   'stock' TEXT NOT NULL, 'shareflow' INTEGER NOT NULL, \
                   'cur_price' NUMERIC NOT NULL, 'trn_price' NUMERIC NOT NULL, \
                   'trn_time' TEXT NOT NULL)",
                   table_id="table_id" + str(session["user_id"]))

        # Redirects to home page
        return redirect("/")
    else:
        return render_template("register.html")


@app.route("/change_pwd", methods=["GET", "POST"])
@login_required
def change_pwd():
    """Change password"""
    if request.method == "POST":
        if not request.form.get("old_pwd"):
            return apology("must provide old password")
        elif not request.form.get("new_pwd"):
            return apology("must provide new password")
        elif not request.form.get("confirmation"):
            return apology("re-type new password as well")

        # Fetch the old password from database
        pwd_hash = db.execute("SELECT hash FROM users WHERE id = :uid", uid=session["user_id"])

        if not check_password_hash(pwd_hash[0]['hash'], request.form.get("old_pwd")):
            return apology("incorrect old password")

        if request.form.get("confirmation") != request.form.get("new_pwd"):
            return apology("re-type new password correctly")
        else:
            # Update the password to the new one
            db.execute("UPDATE users SET hash = :new_hash WHERE id = :uid",
                       new_hash=generate_password_hash(request.form.get("new_pwd")),
                       uid=session["user_id"])

            flash("Password is successfully changed!", 'info')

            return render_template("change_pwd.html")
    else:
        return render_template("change_pwd.html")


def errorhandler(e):
    """Handle error"""
    return apology(e.name, e.code)


# listen for errors
for code in default_exceptions:
    app.errorhandler(code)(errorhandler)
