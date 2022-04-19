from flask import Flask, request, render_template, url_for, redirect, g
import sqlite3

app = Flask(__name__)

app.config['DEBUG'] = True
app.config['SECRET_KEY'] = 'abhishek'

def connect_db():
    sql = sqlite3.connect('C:/Users/abhishek deep/OneDrive/Desktop/database application/data.db')
    sql.row_factory = sqlite3.Row
    return sql

def get_db():
    if not hasattr(g,'sqlite_db'):
        g.sqlite_db = connect_db()
    return g.sqlite_db

@app.teardown_appcontext
def close_db(error):
    if hasattr(g, 'sqlite_db'):
        g.sqlite_db.close()

@app.route('/')
def index():
    return render_template('base.html')


@app.route('/home', methods=['GET', 'POST'])
def home():
    db = get_db()
    cur = db.execute('select Name,Account Number, IFSC Code, Enter Amount, UploadChequeImage from users')
    results = cur.fetchall()

    return render_template('home.html', results=results)

@app.route('/theform', methods=['GET', 'POST'])
def theform():

    if request.method == 'GET':
        return render_template('form.html')
    else:
        Name = request.form['Name']
        AccountNumber = request.form['Account Number']
        IFSCCode = request.form['Enter IFSC Code']
        EnterAmount =request.form['Enter Amount']
        ChooseyourBankName = request.form['Choose your Bank Name']
        UploadChequeImage = request.form['Upload Cheque Image']



        db = get_db()
        db.execute('insert into users (Name, AccountNumber, IFSCCode, EnterAmount, ChooseyourBankName, UploadChequeImage) values (?, ?, ?, ?, ?, ?)', [Name, AccountNumber, IFSCCode,  EnterAmount, ChooseyourBankName, UploadChequeImage])
        db.commit()

        return redirect(url_for('home'))

if __name__ == '__main__':
    app.run()