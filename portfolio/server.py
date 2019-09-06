from flask import Flask, request, make_response, render_template, flash, redirect, url_for
from wtforms import Form, SubmitField, TextField, validators, IntegerField, DecimalField
from DBHandler import DBHandler
from Position import Position
import random


class RegisterForm(Form):
    symbol = TextField('Stock Symbol', [validators.DataRequired(), validators.Length(max=50)])
    num_shares = IntegerField('Number of Shares', [validators.DataRequired()])
    avg_cost = DecimalField('Average Cost', [validators.DataRequired()])
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

        positions = db.db_to_array()

        total = 0

        return render_template("portfolio.html", items=positions, total=total, cartID=None)

    except Exception as e:
        print(e)
        return str("help")


@app.route("/add_position", methods=["GET", "POST"])
def add_position():
    try:
        form = RegisterForm(request.form)

        if request.method == "POST" and form.validate():
            symbol = form.symbol.data
            num_shares = form.num_shares.data
            avg_cost = form.avg_cost.data
            new_position = Position(symbol, num_shares=num_shares, average_cost=avg_cost)
            db.add_position(new_position)

            print(f"Symbol: {symbol}\n Number of shares: {num_shares}\n Average Cost: {avg_cost}")

            return redirect(url_for('view_portfolio'))
        elif request.method == "POST" and not form.validate():
            flash('Error: All the form fields are required. ')

        return render_template("add_position.html", form=form)

    except Exception as e:
        return str(e)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080, debug=True, threaded=True)
