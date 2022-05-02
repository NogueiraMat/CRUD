from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.secret_key = 'Secret Key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:''@localhost/crud_sales'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Sales_Data(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.String(10))
    hour = db.Column(db.String(5))
    status = db.Column(db.String(20))
    value = db.Column(db.Float(5))
    
    def __init__(self, date, hour, status, value):
        self.date = date
        self.hour = hour
        self.status = status
        self.value = value
    
    
@app.route('/')
def index():
    
    get_all_sales = Sales_Data.query.all()
    return render_template("index.html", employees=get_all_sales)


@app.route('/insert_data', methods=['POST'])
def insert_data():
    if request.method == 'POST':
        date = request.form['sale_date']
        hour = request.form['sale_hour']
        status = request.form['sale_status']
        value = request.form['sale_value']    

        sale = Sales_Data(date, hour, status, value)
        db.session.add(sale)
        db.session.commit()
        return redirect(url_for('index'))


@app.route('/update_sale', methods=['GET', 'POST'])
def update_sale():
    if request.method == 'POST':
        new_sale_data = Sales_Data.query.get(request.form.get('id'))
        new_sale_data.date = request.form['sale_date']
        new_sale_data.hour = request.form['sale_hour']
        new_sale_data.status = request.form['sale_status']
        new_sale_data.value = request.form['sale_value']    
        
        db.session.commit()
        return redirect(url_for('index'))


@app.route('/delete_sale/<id>/', methods={'POST', 'GET'})
def delete_sale(id):
    deleted_sale = Sales_Data.query.get(id)
    db.session.delete(deleted_sale)
    db.session.commit()
    return redirect(url_for('index'))
    
    
    
if __name__ == "__main__":
    app.run(debug=True)
