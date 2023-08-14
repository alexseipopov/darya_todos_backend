from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
import sqlalchemy as sa
from flask_cors import CORS

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = 'sqlite:///db.sqlite'

db = SQLAlchemy(app)
CORS(app)


class Todos(db.Model):
    id = sa.Column(sa.Integer, primary_key=True)
    action = sa.Column(sa.Text)
    done = sa.Column(sa.Boolean, default=False)


with app.app_context():
    db.create_all()


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
def update_todos(id):
    item = Todos.query.get(id)
    item.done = not item.done
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
    item.action = request.json.get("action")
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
