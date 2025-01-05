from flask import Flask,render_template,request,redirect
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///data.db"

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Todo(db.Model):
    sno = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    desc = db.Column(db.String(500), nullable=False)

    def __repr__(self) -> str:
        return f"{self.sno} - {self.title}"
    
with app.app_context():
        db.create_all()  # Create all tables

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        title = request.form['title']
        desc = request.form['desc']
        if len(title) != 0:
            todo = Todo(title=title, desc=desc)
            db.session.add(todo)
            db.session.commit()
    allTodo = Todo.query.all()
    return render_template('index.html', allTodo = allTodo)


@app.route('/update/<int:sno>', methods=['GET', 'POST'])
def update(sno):
    if request.method == 'POST':
        title = request.form['title']
        desc = request.form['desc']
        if len(title) != 0:
            todo = Todo.query.filter_by(sno=sno).first()
            todo.title = title
            todo.desc = desc
            db.session.add(todo)
            db.session.commit()
        return redirect('/')

    todo = Todo.query.filter_by(sno=sno).first()
    return render_template('update.html', todo = todo)

@app.route('/delete/<int:sno>')
def delete(sno):
    todo = Todo.query.filter_by(sno=sno).first()
    db.session.delete(todo)
    db.session.commit()
    return redirect('/')


if __name__ == '__main__':
    
    app.run(debug=False)