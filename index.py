import uuid
from flask import Flask, request, jsonify, abort
app = Flask(__name__)

# erstelle einzigartige IDs für listen und einträge
todo_list_1_id = '1318d3d1-d979-47e1-a225-dab1751dbe75'
todo_list_2_id = '3062dc25-6b80-4315-bb1d-a7c86b014c65'
todo_list_3_id = '44b02e00-03bc-451d-8d01-0c67ea866fee'
todo_1_id = str(uuid.uuid4())
todo_2_id = str(uuid.uuid4())
todo_3_id = str(uuid.uuid4())
todo_4_id = str(uuid.uuid4())

todo_lists = [
    {'id': todo_list_1_id, 'name': 'Einkaufsliste'},
    {'id': todo_list_2_id, 'name': 'Arbeit'},
    {'id': todo_list_3_id, 'name': 'Privat'},
]
todos = [
    {'id': todo_1_id, 'name': 'Milch', 'description': '', 'list': todo_list_1_id},
    {'id': todo_2_id, 'name': 'Arbeitsblätter ausdrucken', 'description': '', 'list': todo_list_2_id},
    {'id': todo_3_id, 'name': 'Kinokarten kaufen', 'description': '', 'list': todo_list_3_id},
    {'id': todo_3_id, 'name': 'Eier', 'description': '', 'list': todo_list_1_id},
]

@app.after_request
def apply_cors_header(response):
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Methods'] = 'GET,POST,DELETE,PUT'
    response.headers['Access-Control-Allow-Headers'] = 'Content-Type'
    return response

# Endpunkt zum getten und löschen bestehender Todo-Listen
@app.route('/todo-list/<list_id>', methods=['GET', 'DELETE'])
def handle_list(list_id):
    # find todo list depending on given list id
    list_item = None
    for l in todo_lists:
        if l['id'] == list_id:
            list_item = l
            break
    # if the given list id is invalid, return status code 404
    if not list_item:
        abort(404)
    if request.method == 'GET':
        # find all todo entries for the todo list with the given id
        print('Returning todo list...')
        return jsonify(list_item)
    elif request.method == 'DELETE':
        # delete list with given id
        print('Deleting todo list...')
        todo_lists.remove(list_item)
        for t in todos:
            if t['list'] == list_id:
                todos.remove(t)
        return jsonify({'msg': 'success'}), 200
# Endpunkt zum hinzufügen neuer Listen

@app.route('/todo-list', methods=['POST'])
def add_new_list():
    # make JSON from POST data (even if content type is not set correctly)
    new_list = request.get_json(force=True)
    print('Got new list to be added: {}'.format(new_list))
    # create id for new list, save it and return the list with id
    new_list['id'] = str(uuid.uuid4())
    todo_lists.append(new_list)
    return jsonify(new_list), 200

@app.route('/todo-list/<list_id>/entry', methods=['POST'])
def add_new_entry(list_id):
    list_item = None
    for l in todo_lists:
        if l['id'] == list_id:
            list_item = l
            break
    if list_item == None:
        abort(404)
    # make JSON from POST data (even if content type is not set correctly)
    new_entry = request.get_json(force=True)
    print('Got new entry to be added: {}'.format(new_entry))
    # create id for new entry, save it and return the entry with id
    new_entry['id'] = str(uuid.uuid4())
    new_entry['list'] = list_id
    todos.append(new_entry)
    return jsonify(new_entry), 200


# Endpunkt für das getten von allen Listen, funktioniert
@app.route('/todo-lists', methods=['GET'])
def get_all_lists():
    return jsonify(todo_lists)

# end point for getting all the entries of a given list
@app.route('/todo-list/<list_id>/entries', methods=['GET'])
def get_all_entries(list_id):
    list_entries = []
    for t in todos:
        if t['list'] == list_id:
            entry = {
                'id':t['id'],
                'name':t['name'],
                'description':t['description']
            }
            list_entries.append(entry)
    return jsonify(list_entries)

@app.route('/todo-list/<list_id>/entry/<entry_id>', methods=['PUT', 'DELETE'])
def handle_entry(list_id, entry_id):
    # update or delete a todo-list entry
    entry_item = None
    for t in todos:
        if t['id'] == entry_id and t['list'] == list_id:

            entry_item = t
            #print(entry_item)
            break
    # if the given entry is invalid, return status code 404
    if not entry_item:
        print(entry_item)
        abort(404)
    
        # update entry of given id
        
    elif request.method == "PUT":
        updated_entry = request.get_json(force=True)
        updated_entry['id'] = entry_id
        entry_item.update(updated_entry)
        entry = []
        entry = {
            'id':entry_item['id'],
            'name':entry_item['name'],
            'description':entry_item['description']
        }
        return jsonify(entry_item), 200


    elif request.method == 'DELETE':
        # delete entry of given list with given id
        print('Deleting entry...')
        print(entry_item)
        todos.remove(entry_item)
        return jsonify({'msg': 'success'}), 200


if __name__ == '__main__':
    # start Flask server
    app.debug = True
    app.run(host='127.0.0.1', port=5000)
