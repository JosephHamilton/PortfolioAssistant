from flask import Flask, request, make_response, render_template, flash, redirect, url_for
from wtforms import Form, SubmitField, TextField, validators, IntegerField, DecimalField
from DBHandler import DBHandler
import random


class RegisterForm(Form):
    symbol = TextField('Stock Symbol', [validators.DataRequired(), validators.Length(max=50)])
    num_shares = IntegerField('Number of Shares', [validators.DataRequired(), validators.Length(max=50)])
    avg_cost = DecimalField('Average Cost', [validators.DataRequired(), validators.Length(max=50)], places=2)
    submit = SubmitField("Submit")


app = Flask(__name__)
app.config.from_object(__name__)
app.config['SECRET_KEY'] = '89182haskfna9102u124128924adf9'

db = DBHandler()


@app.route("/", methods=['GET', 'POST'])
@app.route("/portfolio", methods=['GET', 'POST'])
def view_portfolio():
    try:
        if request.method == "POST":
            if request.form["submit_button"] == "add_position":
                return redirect(url_for('add_position'))
            elif request.form["submit_button"] == "shop":
                return redirect(url_for('sell_position'))

        total = 0

        return render_template("portfolio.html", items=None, total=total, cartID=None)

    except Exception as e:
        print(e)
        return str("help")


@app.route("/add_position", methods=["GET", "POST"])
def add_position():
    try:
        form = RegisterForm(request.form)

        if request.method == "POST" and form.validate():
            first_name = form.first_name.data
            last_name = form.last_name.data
            salt = random.randint(1000, 9999)
            id_num = abs(hash(first_name + last_name + str(salt))) % (10 ** 8)

            db.add_user(id_num, first_name, last_name)

            print("First Name:{}\nLast Name:{}\nID Number:{}".format(first_name, last_name, id_num))

            return redirect(url_for('register_rfid', memberID=id_num))
        elif not form.validate():
            flash('Error: All the form fields are required. ')

        return render_template("register.html", form=form)

    except Exception as e:
        return str(e)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080, debug=True, threaded=True)
