from models import app, User, Post, Tag, get_or_create
from flask import jsonify, request
from helpers import
from models import Publisher, Genre, Game
def error(err_locale, error):
    print(f"🔥 Error in {err_locale}\n{error}")
    return jsonify(error='Server Error')

# index
def get_all_publisher():
    try:
        all_publishers = User.query.all()
        results = [publisher.as_dict() for publisher in all_publishers]
        return jsonify(results)
    except Exception as error:
        return error('getting all publishers', error)

# show
def get_publisher(id):
    try:
        publisher = Publisher.query.get(id)
        if publisher:
            return jsonify(publisher.as_dict())
        else:
            return error('getting publisher', 'No publisher at that id')
            raise Exception(f'Error getting publisher at id {id}')
    except Exception as error:
        return error('getting one publisher', error)

# create
def create_publisher(name):
    try:
        new_publisher = Publisher(name=name)
        db.session.add(new_publisher)
        db.session.commit()
        return jsonify(new_publisher.as_dict())
    except Exception as error:
        return error('creating a new publisher', error)
# update
def update_publisher(id, name):
    try:
        publisher = Publisher.query.get(id)
        if publisher:
            publisher.name = name or publisher.name
            db.session.commit()
            return jsonify(publisher.as_dict())
        else:
            return error('update publisher', 'No publisher at that id')
    except Exception as error:
        return error('updating a publisher', error)
# destroy
def destroy_publisher(id):
    try:
        publisher = Publisher.query.get(id)
        if publisher:
            db.session.delete(publisher)
            db.session.commit()
            return redirect('/publisher')
        else:
            return error('destroying publisher', 'No publisher at that id')
    except Exception as error:
        return error('deleting a publisher', error)


@app.errorhandler(Exception)
def unhandled_exception(e):
    app.logger.info('Unhandled exception: %s', (e))
    message_str = e.__str__()
    return jsonify(message=message_str.split(':')[0])

@app.route('/')
def home():
    first_publisher = Publisher.query.first()
    return jsonify(user=first_publisher.as_dict())

@app.route('/publisher', methods=['GET','POST'])
def user_index_create():
    if request.method == 'GET':
        try: 
            return get_all_publisher()
        except Exception as error:
            return error('GET /publisher route', error)
    elif request.method == 'POST':
        try: 
            return create_publisher(name=request.form['name'])
        except Exception as error:
            return error('POST /users route', error)

@app.route('/publisher/<int:id>', methods=['GET', 'PUT', 'DELETE'])
def publisher_show_update_delete(id):
    if request.method == 'GET':
        # 
        try:
            return get_publisher(id)
        except Exception as error:
            return error('GET /publisher/:id route', error)
    if request.method == 'PUT':
        try:
            return update_publisher(id = id, name=request.form['name'])
        except Exception as error:
            return error('PUT /publisher/id route', error)
    if request.method == 'DELETE':
        # 
        try:
            return destroy_publisher(id)
        except Exception as error:
            return error('DELETE /publisher:id route', error)
