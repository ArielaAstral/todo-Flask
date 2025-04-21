from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']="sqlite:///todo.db"

db=SQLAlchemy(app)

class Todo(db.Model):
    Sno=db.Column(db.Integer,primary_key=True)
    title=db.Column(db.String(100),nullable=True)
    desc=db.Column(db.String(500),nullable=True)
    date_created=db.Column(db.DateTime,default=datetime.now)

    def __repr__(self)->str:
        return f"{self.Sno}-{self.title}"

@app.route("/",methods=['GET','POST'])
def hello_world():
    if request.method=='POST':
        title=request.form['title']
        desc=request.form['desc']
        todo=Todo(title=title,desc=desc)
        db.session.add(todo)
        db.session.commit()
        return redirect(url_for('hello_world'))  # redirect after POST
    alltodo=Todo.query.all()
    return render_template('index.html',alltodo=alltodo)

@app.route("/delete/<int:Sno>")
def delete(Sno):
    todel=Todo.query.filter_by(Sno=Sno).first()
    db.session.delete(todel)
    db.session.commit()
    return redirect('/')

@app.route("/update/<int:Sno>",methods=['GET','POST'])
def update(Sno):
    if request.method=='POST':
        title =request.form['title']
        desc = request.form['desc']
        toup=Todo.query.filter_by(Sno=Sno).first()
        toup.title=title
        toup.desc=desc
        db.session.commit()
        return redirect('/')

    toup=Todo.query.filter_by(Sno=Sno).first()
    return render_template('update.html',toup=toup)
if __name__ == '__main__':
    app.run(debug=True)