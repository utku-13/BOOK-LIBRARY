from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

##CREATE DATABASE 
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///new-book-collection.db"
#Optional: But it will silence the deprecation warning in the console.
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


##CREATE TABLE
class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(250), unique=True, nullable=False)
    author = db.Column(db.String(250), nullable=False)
    rating = db.Column(db.Float, nullable=False)

    #Optional: this will allow each book object to be identified by its title when printed.
    def __repr__(self):
        return f'{self.title}-{self.author}-{self.rating}'
    
with app.app_context():
    db.create_all()

all_books = []


@app.route('/')
def home():
    
    with app.app_context():    
        all_books = db.session.query(Book).all()
    return render_template('index.html', books = all_books)


@app.route("/add",methods=['GET','POST'])
def add():
    if request.method == 'POST':
        #CREATE RECORD
        with app.app_context():   
            new_book = Book(title=request.form.get('bn'), author=request.form.get('ba'), rating=request.form.get('br'))
            db.session.add(new_book)
            db.session.commit()
        print(all_books)
        return redirect(url_for('home'))
    return render_template('add.html')

@app.route('/editrating<id>',methods=['GET','POST'])
def edit_rating(id):
    if request.method == 'POST':
        with app.app_context():
            book_to_update = db.session.execute(db.select(Book).where(Book.id == id)).scalar()
            # or book_to_update = db.session.get(Book, book_id)  
            # Note Book.query.get() is deprecated
            book_to_update.rating = request.form.get('rating')
            db.session.commit()
        return redirect(url_for('home'))
    with app.app_context():
        all_books = db.session.query(Book).all()
    return render_template('edit.html',id=id,book=all_books[int(id)-1])

@app.route('/delete<id>')
def delete(id):
    with app.app_context():
        book_to_delete = db.session.execute(db.select(Book).where(Book.id == id)).scalar()
        db.session.delete(book_to_delete)
        db.session.commit()
    return redirect(url_for('home')) 

if __name__ == "__main__":
    app.run(debug=True)

