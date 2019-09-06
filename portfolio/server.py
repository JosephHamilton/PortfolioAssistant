from flask import Flask, request, make_response, render_template, flash, redirect, url_for
from wtforms import Form, SubmitField, TextField, validators, IntegerField, DecimalField, SelectField
from DBHandler import DBHandler
from Position import Position

db = DBHandler()


class AddPosition(Form):
    symbol = TextField('Stock Symbol', validators=[validators.DataRequired(), validators.Length(max=50)])
    num_shares = IntegerField('Number of Shares', validators=[validators.DataRequired()])
    avg_cost = DecimalField('Average Cost', places=2, validators=[validators.DataRequired()])
    submit = SubmitField("Submit")


class SellPosition(Form):
    current_positions = db.current_positions()

    symbol = SelectField('Stock Symbol', choices=[('current_positions', 'wwwa'), ('test', 'nana')])
    num_shares = IntegerField('Number of Shares', validators=[validators.DataRequired()])
    avg_cost = DecimalField('Average Cost', places=2, validators=[validators.DataRequired()])
    submit = SubmitField("Submit")


app = Flask(__name__)
app.config.from_object(__name__)
app.config['SECRET_KEY'] = '89182haskfna9102u124128924adf9'


@app.route("/", methods=['GET', 'POST'])
@app.route("/portfolio", methods=['GET', 'POST'])
def view_portfolio():
    try:
        if request.method == "POST":
            if request.form["submit_button"] == "add_position":
                return redirect(url_for('add_position'))
            elif request.form["submit_button"] == "sell_position":
                return redirect(url_for('sell_position'))

        positions = db.db_to_array()

        total = 0

        for position in positions:
            total += position.totalInvestment

        return render_template("portfolio.html", positions=positions, total=total)

    except Exception as e:
        print(e)
        return str("Error Occurred")


@app.route("/add_position", methods=["GET", "POST"])
def add_position():
    try:
        form = AddPosition(request.form)

        if request.method == "POST" and form.validate():
            symbol = form.symbol.data
            num_shares = form.num_shares.data
            avg_cost = form.avg_cost.data
            new_position = Position(symbol, num_shares=num_shares, average_cost=avg_cost)

            db.add_position(new_position)

            return redirect(url_for('view_portfolio'))
        elif request.method == "POST" and not form.validate():
            flash('Error: All the form fields are required. ')

        return render_template("add_position.html", form=form)

    except Exception as e:
        return str(e)


@app.route("/sell_position", methods=["GET", "POST"])
def sell_position():
    try:
        form = SellPosition(request.form)

        if request.method == "POST" and form.validate():
            symbol = form.symbol.data
            num_shares = form.num_shares.data
            avg_cost = form.avg_cost.data
            new_position = Position(symbol, num_shares=num_shares, average_cost=avg_cost)

            db.sell_position(new_position)

            return redirect(url_for('view_portfolio'))
        elif request.method == "POST" and not form.validate():
            flash('Error: All the form fields are required. ')

        return render_template("sell_position.html", form=form)

    except Exception as e:
        return str(e)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080, debug=True, threaded=True)
