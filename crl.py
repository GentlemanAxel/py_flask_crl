from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///localharvesthub.db'
db = SQLAlchemy(app)

class Producer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(80), nullable=False)
    last_name = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(80), nullable=False)
    production_type = db.Column(db.String(80), nullable=False)
    harvest_date = db.Column(db.DateTime, nullable=False)
    location = db.Column(db.String(120), nullable=False)

    def __repr__(self):
        return f'<Producer {self.last_name}>'

@app.route('/')
def index():
    producers = Producer.query.order_by(Producer.harvest_date).all()
    return render_template('index.html', producers=producers)

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        email = request.form['email']
        password = request.form['password']
        production_type = request.form['production_type']
        harvest_date = datetime.strptime(request.form['harvest_date'], '%Y-%m-%d')
        location = request.form['location']

        new_producer = Producer(first_name=first_name, last_name=last_name, email=email, password=password,
                                production_type=production_type, harvest_date=harvest_date, location=location)
        db.session.add(new_producer)
        db.session.commit()
        return redirect(url_for('index'))

    return render_template('register.html')

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
