from flask import Flask, request, jsonify, make_response
from flask_sqlalchemy import SQLAlchemy
import uuid
from werkzeug.security import generate_password_hash, check_password_hash
import jwt
import datetime
from functools import wraps


app = Flask(__name__)

app.config['SECRET_KEY'] = 'This is Joseph'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///./todo.db'

db = SQLAlchemy(app)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    public_id = db.Column(db.String(50), unique=True)
    name = db.Column(db.String(50))
    password = db.Column(db.String(50))
    admin = db.Column(db.Boolean)


class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(100))
    complete = db.Column(db.Boolean)
    user_id = db.Column(db.Integer)


def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None

        if 'x=access-token' in request.headers:
            token = request.header['x-access-token']

        if not token:
            return jsonify({'Message': 'Token is missing'})

        try:
            data = jwt.decode(token, app.config['SECRET_KEY'])
            current_user = User.query.filter_by(public_id=data['public_id']).first()
        except:
            return jsonify({'Message': 'Token is Invalid'})

        return f(current_user, *args, **kwargs)

    return decorated


@app.route('/user', methods=["GET"])
@token_required
def get_all_users(current_user):

    """After getting a token, only admin users can perform these operations"""
    if not current_user.admin:
        return jsonify({'Message': 'can not perform that function'})
    users = User.query.all()

    """i want to store them in a dictionary since i cant jsonify them"""
    output = []

    """loop through all users"""
    for user in users:
        user_data = {}
        user_data['public_id'] = user.public_id
        user_data['name'] = user.name
        user_data['password'] = user.password
        user_data['admin'] = user.admin
        output.append(user_data)
    return jsonify({'user': output})


@app.route('/user/<public_id>', methods=["GET"])
@token_required
def get_one_user(current_user, public_id):

    """After getting a token, only admin users can perform these operations"""
    if not current_user.admin:
        return jsonify({'Message': 'can not perform that function'})

    user = User.query.filter_by(public_id=public_id).first()

    if not user:
        return jsonify({'message': 'No user found'})

    user_data = {}
    user_data['public_id'] = user.public_id
    user_data['name'] = user.name
    user_data['password'] = user.password
    user_data['admin'] = user.admin
    return jsonify({'Message': user_data})


@app.route('/user', methods=["POST"])
@token_required
def create_user(current_user):

    """After getting a token, only admin users can perform these operations"""
    if not current_user.admin:
        return jsonify({'Message': 'can not perform that function'})

    data = request.get_json()
    hashed_password = generate_password_hash(data['password'], method="sha256")

    new_user = User(public_id=str(uuid.uuid4()), name=data['name'], password=hashed_password, admin=False)
    db.session.add(new_user)
    db.session.commit()

    return jsonify({'message': 'The New User has been created'})


@app.route('/user/<public_id>', methods=["PUT"])
@token_required
def promote_user(current_user, public_id):
    """After getting a token, only admin users can perform these operations"""
    if not current_user.admin:
        return jsonify({'Message': 'can not perform that function'})

    user = User.query.filter_by(public_id=public_id).first()

    if not user:
        return jsonify({'Message': 'No user found'})
    user.admin = True
    db.session.commit()
    return jsonify({'Message': 'The user has been promoted'})


@app.route('/user/<public_id>', methods=["DELETE"])
@token_required
def delete_user(current_user, public_id):

    """After getting a token, only admin users can perform these operations"""
    if not current_user.admin:
        return jsonify({'Message': 'can not perform that function'})

    user = User.query.filter_by(public_id=public_id).first()

    if not user:
        return jsonify({'Message': 'User doesnt exist'})
    db.session.delete(user)
    db.session.commit()
    return jsonify({'Message': 'The user has been deleted'})


@app.route('/login')
def login():
    """"If user exists, he will get a token. here we check his credentials"""
    auth = request.authorization

    if not auth or not auth.username or not auth.password:
        return make_response('could not verify', 401, {'WWW-Authenticate': 'Basic realm="Login required!"'})

    user = User.query.filter_by(name=auth.username).first()

    if not user:
        return make_response('could not verify', 401, {'WWW-Authenticate': 'Basic realm="Login required!"'})
    if check_password_hash(user.password, auth.password):
        token = jwt.encode({'public_id': user.public_id, 'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=30)}, app.config['SECRET_KEY'])

        return jsonify({'token': token.decode('UTF-8')})

    return make_response('could not verify', 401, {'WWW-Authenticate': 'Basic realm="Login required!"'})


"""The routes for the todos"""


@app.route('/todo', methods=['GET'])
@token_required
def get_all_todos(current_user):
    todos = Todo.query.filter_by(user_id = current_user.id).all()

    output = []

    for todo in todos:
        todo_data = {}
        todo_data['id'] = todo.id
        todo_data['text'] = todo.text
        todo_data['complete'] = todo.complete
        output.append(todo_data)

    return jsonify({'todos': output})


@app.route('/todo/<todo_id>', methods=['GET'])
@token_required
def get_one_todo(current_user, todo_id):
    todo = Todo.query.filterby(id=todo_id, user_id=current_user.id).first()

    if not todo:
        return jsonify({'Message': 'No to do found, please add some'})

    todo_data = {}
    todo_data['id'] = todo.id
    todo_data['text'] = todo.text
    todo_data['complete'] = todo.complete

    return jsonify({'Message': todo_data})


@app.route('/todo/<todo_id>', methods=['POST'])
@token_required
def create_todo(current_user, todo_id):
    data = request.get_json()

    new_todo = Todo(text=data['text'], complete=False, user_id=current_user.id)
    db.session.add(new_todo)
    db.session.commit()

    return jsonify({'Message': 'Todo Created Successfully'})


@app.route('todo/<todo_id>', methods=['PUT'])
@token_required
def complete_todo(current_user, todo_id):
    todo = Todo.query.filterby(id=todo_id, user_id=current_user.id).first()

    if not todo:
        return jsonify({'Message': 'No to do found, please add some'})

    todo.complete = True
    db.session.commit()
    return jsonify({'Message': 'Todo has been completed'})


@app.route('todo/<todo_id>', methods=['DELETE'])
@token_required
def delete_todo(current_user, todo_id)
    todo = Todo.query.filter_by(id=todo_id, user_id=current_user).first()

    if not todo:
        return jsonify({'Message': 'No todo found'})

    db.session.delete(todo)
    db.session.commit()

    return jsonify({'Message': 'Todo has been deleted successfully'})


if __name__ == '__main__':
    app.run(debug=True)
