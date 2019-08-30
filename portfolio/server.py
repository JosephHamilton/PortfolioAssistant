from flask import Flask, request, make_response, render_template, flash, redirect, url_for
from wtforms import Form, SubmitField, TextField, validators, IntegerField, DecimalField
from DBHandler import DBHandler
import netifaces as ni
from zeroconf import ServiceInfo, Zeroconf
import socket
import random
import pickle

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
def cart():

    try:
        total = 0

        return render_template("portfolio.html", items=None, total=total, cartID=None)

    except Exception as e:
        print(e)
        return str("help")


if __name__ == "__main__":
    # Find ip address to broadcast with zeroconf
    # ipAddress = ni.ifaddresses('wlan0')[ni.AF_INET][0]['addr']

    # Create register qr code
    # server_ip = ipAddress
    
    app.run(host="0.0.0.0", port=8080, debug=True, threaded=True)
