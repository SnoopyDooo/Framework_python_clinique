"""
les imports
"""
from flask import Flask, redirect, render_template, url_for, request, flash
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.secret_key = "djfljdfljfnkjdfhjfshjkfjfjfhhjdhdjhdfu"

"""
information de connexion à la base de données
"""

userpass = "mysql+pymysql://root:@"
basedir = "127.0.0.1"
dbname = "/clinique"

app.config["SQLALCHEMY_DATABASE_URI"] = userpass + basedir + dbname
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)

class Patients(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    tel = db.Column(db.String(50), nullable=False)
    address = db.Column(db.String(255), nullable=False)
    maladie = db.Column(db.String(255), nullable=False)

    def __init__(self, name, email, tel, address, maladie):
        self.name = name
        self.email = email
        self.tel = tel
        self.address = address
        self.maladie = maladie

"""
Les routes
"""

@app.route('/')
def index():
    data_patient = db.session.query(Patients)
    return render_template("index.html", data=data_patient)

"""
les actions pour input
"""

@app.route('/input', methods=['GET', 'POST'])
def input_data():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        tel = request.form['tel']
        address = request.form['address']
        maladie = request.form['maladie']

        add_data = Patients(name, email, tel, address, maladie)

        db.session.add(add_data)
        db.session.commit()

        flash(': le patient a été ajouté')

        return redirect(url_for('index'))

    return render_template('input.html')

"""
les actions pour edit
"""

@app.route('/edit/<int:id>')
def edit_data(id):
    data_Patients = Patients.query.get(id)
    return render_template('edit.html', data=data_Patients)

@app.route('/proses_edit', methods=['POST'])
def proses_edit():
    id = request.form.get('id')
    data_patient = Patients.query.get(id)

    data_patient.name = request.form['name']
    data_patient.email = request.form['email']
    data_patient.tel = request.form['tel']
    data_patient.address = request.form['address']
    data_patient.maladie = request.form['maladie']

    db.session.commit()

    flash(': les informations ont été modifier')

    return redirect(url_for('index'))

"""
Les actions pour delete
"""

from flask import redirect, url_for, abort

@app.route('/delete/<int:id>')
def delete(id):
    data_patient = Patients.query.get(id)

    if data_patient is None:
        flash("patient data with ID {} not found.".format(id))
        return redirect(url_for('index'))

    db.session.delete(data_patient)
    db.session.commit()

    flash(": le patient a été supprimer")
    return redirect(url_for('index'))



if __name__ == "__main__":
    app.run(debug=True)
