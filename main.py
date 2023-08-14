import sqlalchemy as sa
from flask import Flask, request
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = 'sqlite:///db.sqlite'
app.config["SECRET_KEY"] = "secret key"

db = SQLAlchemy(app)
CORS(app)

admin = Admin(app)


class Todos(db.Model):
    id = sa.Column(sa.Integer, primary_key=True)
    action = sa.Column(sa.Text)
    done = sa.Column(sa.Boolean, default=False)


with app.app_context():
    db.create_all()


class TodosIndexView(ModelView):
    pass


admin.add_view(TodosIndexView(Todos, db.session, name='Todos'))


@app.get('/todos')
def get_todos():
    todos = Todos.query.all()
    return {
        "status": 0,
        "description": "OK",
        "data": {
            "todos": [{
                "id": item.id,
                "action": item.action,
                "done": item.done
            } for item in todos]
        }
    }


@app.post('/add_todos')
def add_todos():
    action = request.form.get("action")
    item = Todos(action=action)
    db.session.add(item)
    db.session.commit()
    return {
        "status": 0,
        "description": "OK",
        "data": {
            "todos": {
                "id": item.id,
                "action": item.action,
                "done": item.done
            }
        }
    }


@app.put('/todos/<int:id>')
def change_todos(id):
    item = Todos.query.get(id)
    action = request.json.get("action")
    done = request.json.get("done")
    item.action = action if action else item.action
    item.done = not done if done else item.done
    db.session.commit()
    return {
        "status": 0,
        "description": "OK",
        "data": {
            "todos": {
                "id": item.id,
                "action": item.action,
                "done": item.done
            }
        }
    }


@app.delete('/todos/<int:id>')
def delete_todos(id):
    item = Todos.query.get(id)
    db.session.delete(item)
    db.session.commit()
    return {
        "status": 0,
        "description": "OK",
        "data": {
            "todos": {
                "id": item.id,
                "action": item.action,
                "done": item.done
            }
        }
    }


if __name__ == '__main__':
    app.run(port=5000, debug=True)
