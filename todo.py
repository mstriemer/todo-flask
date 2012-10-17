from flask import Flask, jsonify, request
app = Flask(__name__)

class TodoRepository(object):
    def __init__(self):
        self.todos = []

    def all(self):
        return filter(lambda t: t is not None, self.todos)

    def save(self, todo):
        todo.id = len(self.todos) + 1
        self.todos.append(todo)

    def find(self, id):
        if 0 <= id - 1 < len(self.todos):
            todo = self.todos[id - 1]
        else:
            todo = None
        return todo

    def remove(self, todo):
        index = todo.id - 1
        if self.todos[index] == todo:
            self.todos[index] = None
        else:
            raise ArgumentError("invalid todo")

class Todo(object):
    def __init__(self, name):
        self.name = name
        self.id = None

    def as_dict(self):
        return dict(id=self.id, name=self.name)

todo_repository = TodoRepository()
todo_repository.save(Todo("Learn Flask"))
todo_repository.save(Todo("Make an API"))

@app.route('/', methods=['GET'])
def index():
    todos = [todo.as_dict() for todo in todo_repository.all()]
    return jsonify(todos=todos)

@app.route('/<id>/', methods=['GET'])
def show(id):
    id = int(id)
    todo = todo_repository.find(id)
    if todo is None:
        return "Not Found", 404
    else:
        return jsonify(todo.as_dict())

@app.route('/<id>/', methods=['DELETE'])
def destroy(id):
    id = int(id)
    todo = todo_repository.find(id)
    if todo is None:
        return "Not Found", 404
    else:
        todo_repository.remove(todo)
        return '', 204

@app.route('/', methods=['POST'])
def create():
    name = request.form.get('name', '')
    if not name:
        return "name is required", 322
    else:
        todo = Todo(name)
        todo_repository.save(todo)
        return jsonify(todo.as_dict()), 201

if __name__ == '__main__':
    app.run(debug=True)
