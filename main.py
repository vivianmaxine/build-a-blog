from flask import Flask, request, redirect, render_template
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = \
    'mysql+pymysql://build-a-blog:build-a-blog@localhost:8889/build-a-blog'
app.config['SQLALCHEMY_ECHO'] = True

db = SQLAlchemy(app)  # creates database object


class BlogPost(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120))
    entry = db.Column(db.String(50000))

    def __init__(self, title, entry):
        self.title = title
        self.entry = entry

    def __repr__(self):
        return '<BlogPost %r>' % self.title


@app.route('/', methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        post_title = request.form['title']
        post_entry = request.form['entry']

        new_post = BlogPost(title=post_title, entry=post_entry)

        db.session.add(new_post)
        db.session.commit()

    posts = BlogPost.query.all()

    return render_template('index.html', title="Vivian's Blog", posts=posts)


if __name__ == "__main__":
    app.run()
