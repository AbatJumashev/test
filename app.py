from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:Aksay_2023@localhost/postgres'
db = SQLAlchemy(app)
migrate = Migrate(app, db)

# one table in database, Model==Table
class Item(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)

@app.route('/')
def index():
    items = Item.query.all()# Select * from Item;
    return render_template('index.html', items=items)

@app.route('/create', methods=['POST', 'GET'])
def create():# request.method =='POST'
    if request.method == 'POST':
        item_name = request.form['name']
        new_item = Item(name=item_name)
        db.session.add(new_item)# adds item
        db.session.commit() # saves changes
        return redirect(url_for('index'))
    return render_template('create.html')

@app.route('/update/<int:id>', methods=['POST', 'GET'])
def update(id):
    item = Item.query.get(id) # select * from Item where Item.id = id
    if request.method == 'POST':
        item.name = request.form['name']
        db.session.commit()# save changes
        return redirect(url_for('index'))
    return render_template('update.html', item=item)

@app.route('/delete/<int:id>')
def delete(id): # id = item.id
    item = Item.query.get(id) # Select * from Item where Item.id = id
    db.session.delete(item)
    db.session.commit()
    return redirect(url_for('index'))

@app.route('/delete_multiple', methods=['POST'])
def delete_multiple():
    task_ids = request.form.getlist('task_ids')
    for task_id in task_ids:
        item = Item.query.get(int(task_id))
        db.session.delete(item)

    db.session.commit()
    return redirect(url_for('index'))

