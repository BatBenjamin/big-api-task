import uuid
from flask import Flask, request, jsonify, abort
app = Flask(__name__)

# erstelle einzigartige IDs für listen und einträge zu Test- und Demonstrationszwecken
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
    list_item = None
    for l in todo_lists:
        if l['id'] == list_id:
            list_item = l
            break
    # Fehlermeldung wenn liste nicht gegeben
    if not list_item:
        abort(404)
    if request.method == 'GET':
        # Finde die spezifische Liste
        print('Returning todo list...')
        return jsonify(list_item)
    elif request.method == 'DELETE':
        # Lösche Liste mit der ID, inklusive aller Einträge
        print('Deleting todo list...')
        todo_lists.remove(list_item)
        for t in todos:
            if t['list'] == list_id:
                todos.remove(t)
        return jsonify({'msg': 'success'}), 200
    
# Endpunkt zum hinzufügen neuer Listen
@app.route('/todo-list', methods=['POST'])
def add_new_list():
    # Erstelle eine neue Liste
    new_list = request.get_json(force=True)
    print('Got new list to be added: {}'.format(new_list))
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
    # Erstelle neuen Eintrag der Liste
    new_entry = request.get_json(force=True)
    print('Got new entry to be added: {}'.format(new_entry))
    new_entry['id'] = str(uuid.uuid4())
    new_entry['list'] = list_id
    todos.append(new_entry)
    return jsonify(new_entry), 200


# Endpunkt für das getten von allen Listen
@app.route('/todo-lists', methods=['GET'])
def get_all_lists():
    return jsonify(todo_lists)

# Endpunkt zum Erhalten aller Einträge einer Liste
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
    # update oder lösche Todo-Listeneintrag
    entry_item = None
    for t in todos:
        if t['id'] == entry_id and t['list'] == list_id:
            entry_item = t
            break
    # wenn kein Eintrag, gieb Fehler 404 zurück.
    if not entry_item:
        print(entry_item)
        abort(404)
    
        # update Eintrag unter den gegebenen IDs
        
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
        # Lösche den Eintrag in der Liste basierend auf Listen- und Eintrags-ID
        print('Deleting entry...')
        print(entry_item)
        todos.remove(entry_item)
        return jsonify({'msg': 'success'}), 200


if __name__ == '__main__':
    # starte Flask server
    app.debug = True
    app.run(host='127.0.0.1', port=5000)
