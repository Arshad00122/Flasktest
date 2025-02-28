import os
from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# Ensure the database folder exists
db_folder = os.path.join(os.getcwd(), "database")
if not os.path.exists(db_folder):
    os.makedirs(db_folder)

# Define the database path
db_path = os.path.join(db_folder, 'users.db')

# Make sure SQLALCHEMY_DATABASE_URI is set
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{db_path}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Debugging step: Check if URI is correctly set
print("Database URI:", app.config['SQLALCHEMY_DATABASE_URI'])  # <-- Add this line

# Initialize SQLAlchemy
db = SQLAlchemy(app)

app.secret_key = "your-very-secret-key"

# Define a simple model
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(80), nullable=False)

# Create tables within app context
with app.app_context():
    db.create_all()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/index2')
def index2():
    return render_template('index2.html')

@app.route('/Login', methods=['GET', 'POST'])
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # Check if the username already exists
        existing_user = User.query.filter_by(username=username).first()
        if existing_user:
            flash("Username already exists! Please choose another one.", "error")
            return redirect(url_for('login'))

        new_user = User(username=username, password=password)
        db.session.add(new_user)
        db.session.commit()
        flash("Successfully registered!", "success")
        return redirect(url_for('login'))
    
    return render_template('login.html')


@app.route('/user')
def show_user():
    users = User.query.all()
    return render_template('user.html',users=users)
    


if __name__ == '__main__':
    app.run(debug=True)
