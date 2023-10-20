import functools
from threading import Thread
import os

from flask import Flask, render_template, request, session, copy_current_request_context
import time
from dbconnector import CreateMySQLCursor, DBConnectionError, DBCredentialsError, DBSQLError
from services import do_something

app = Flask(__name__)

app.secret_key = os.getenv("SECRET_KEY", "123123")

app.config["dbconfig"] = {
    "host": os.getenv("MYSQL_HOST"),
    "user": os.getenv("MYSQL_USER"),
    "password": os.getenv("MYSQL_PASSWORD"),
    "database": os.getenv("MYSQL_DATABASE")
}



# print(app.config["dbconfig"])

def check_logged_in(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        if session.get("logged_in"):
            return func(*args, **kwargs)
        return "Access restricted"

    return wrapper


@app.route("/login")
def do_login() -> str:
    session['logged_in'] = True
    return "You are logged in"


@app.route("/logout")
def do_logout() -> str:
    session['logged_in'] = False
    return "You are logged out"


@app.route("/process", methods=["POST"])
def process_data() -> str:
    @copy_current_request_context
    def log_request(req, res: str):
        time.sleep(2)
        try:
            with CreateMySQLCursor(app.config["dbconfig"]) as cursor:
                data1 = req.form["input1"]
                data2 = req.form["input2"]
                query = "insert into log (data1, data2, ip, browser_string, results) values (%s, %s, %s, %s, %s);"
                cursor.execute(query, (data1, data2, req.remote_addr, req.user_agent.string, res,))
        except DBConnectionError as err:
            print("DB connection error", str(err))
        except DBCredentialsError as err:
            print("DB credentials error", str(err))
        except DBSQLError as err:
            print("DB query error", str(err))

    input1 = request.form["input1"]
    input2 = request.form["input2"]
    result = do_something(input1, input2)
    try:
        t = Thread(target=log_request, args=(request, result))
        t.start()
        # time.sleep(300)
        # log_request(request, result)
        return render_template("result.html", the_title="Result page", the_results=result, input1=input1, input2=input2)

    except Exception as err:
        print("Something went wrong", str(err))
    return "Error"


@app.route("/")
@app.route("/entry")
def entry() -> str:
    return render_template("entry.html", the_title="Main page")


@app.route("/viewlog")
@check_logged_in
def view_log() -> str:
    try:
        with CreateMySQLCursor(app.config["dbconfig"]) as cursor:
            query = "select * from log"
            cursor.execute(query)
            log_data = cursor.fetchall()
        return render_template("view_logs.html", the_title="Log",
                               the_row_titles=["id", "timestamp", "data1", "data2", "remote addr", "user agent",
                                               "results"],
                               the_data=log_data
                               )
    except DBConnectionError as err:
        print("DB connection error", str(err))
    except DBCredentialsError as err:
        print("DB credentials error", str(err))
    except DBSQLError as err:
        print("DB query error", str(err))
    except Exception as err:
        print("Something went wrong", str(err))
    except BaseException as err:
        print("Something BASE went wrong", str(err))
    return "Error"


# @app.route("/test")
# def test():
#     return "<script type='test/javascript'>alert('Hello');</script>"


if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0")
