from flask import Flask, jsonify
app = Flask(__name__)

class TodoRepository(object):
    def __init__(self):
        self.todos = []

    def all(self):
        return self.todos

    def save(self, todo):
        todo.id = len(self.todos) + 1
        self.todos.append(todo)

class Todo(object):
    def __init__(self, name):
        self.name = name
        self.id = None

    def as_dict(self):
        return dict(id=self.id, name=self.name)

todo_repository = TodoRepository()
todo_repository.save(Todo("Learn Flask"))
todo_repository.save(Todo("Make an API"))

@app.route('/')
def index():
    todos = [todo.as_dict() for todo in todo_repository.all()]
    return jsonify(todos=todos)

if __name__ == '__main__':
    app.run()
