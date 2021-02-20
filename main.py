from flask import Flask, render_template, redirect
from wtforms import validators
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField
from wtforms.validators import DataRequired
import csv


app = Flask(__name__)
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
Bootstrap(app)


class CafeForm(FlaskForm):
    cafe = StringField('Cafe name', validators=[DataRequired()])
    url = StringField('URL', validators=[DataRequired(), validators.URL()])
    open_time = StringField('Open Time', validators=[DataRequired()])
    closing_time = StringField('Closing Time', validators=[DataRequired()])
    coffee_rating = SelectField('Coffee Rating', choices=[("☕"), ("☕ ☕"), ("☕ ☕ ☕"), ("☕ ☕ ☕ ☕")], validators=[DataRequired()])
    wifi_rating = SelectField('Wifi Rating', choices=[("💪"), ("💪💪"), ("💪💪💪"), ("💪💪💪💪")],validators=[DataRequired()])
    power_outlet = SelectField('Power Outlet', choices=[("🔌"), ("🔌🔌"), ("🔌🔌🔌"), ("🔌🔌🔌🔌")], validators=[DataRequired()])
    submit = SubmitField('Submit')


@app.route("/")
def home():
    return render_template("index.html")


@app.route('/add', methods=['GET', 'POST'])
def add_cafe():
    form = CafeForm()
    if form.validate_on_submit():
        database = []
        with open("cafe-data.csv", "a", newline='', encoding="utf8") as csv_file:
            writer = csv.writer(csv_file, delimiter=",")
            for value in form:
                database.append(value.data)
            writer.writerow(database[:-2])
            return redirect("cafes")
    return render_template('add.html', form=form)


@app.route('/cafes')
def cafes():
    with open('cafe-data.csv', newline='', encoding="utf8") as csv_file:
        csv_data = csv.reader(csv_file, delimiter=',')
        list_of_rows = []
        for row in csv_data:
            list_of_rows.append(row)
    return render_template('cafes.html', cafes=list_of_rows)


if __name__ == '__main__':
    app.run(debug=True)
