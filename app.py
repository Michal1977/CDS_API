from flask import Flask, jsonify, abort, make_response, request
from models import cds

app = Flask(__name__)
app.config["SECRET_KEY"] = "nininini"


@app.route("/api/v1/cds/", methods=["GET"])
def cds_list_api_v1():
    return jsonify(cds.all())


@app.route("/api/v1/cds/<int:cd_id>", methods=["GET"])
def get_cd(cd_id):
    cd = cds.get(cd_id)
    if not cd:
        abort(404)
    return jsonify({"cd": cd})


@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found', 'status_code': 404}), 404)


@app.route("/api/v1/cds/", methods=["POST"])
def create_cd():
    if not request.json or not 'name' or not 'title' in request.json:
        abort(400)
    cd = {
        'id': cds.all()[-1]['id'] + 1,
        'name': request.json['name'],
        'title': request.json['title'],
        'year': request.json.get('year', ''),
        }
    cds.create(cd)
    return jsonify({'cd': cd}), 201


@app.route("/api/v1/cds/<int:cd_id>", methods=['DELETE'])
def delete_cd(cd_id):
    result = cds.delete(cd_id)
    if not result:
        abort(404)
    return jsonify({'result': result})


@app.route("/api/v1/cds/<int:cd_id>", methods=["PUT"])
def update_cd(cd_id):
    cd = cds.get(cd_id)
    if not cd:
        abort(404)
    if not request.json:
        abort(400)
    data = request.json
    if any([
        'name' in data and not isinstance(data.get('name'), str),
        'title' in data and not isinstance(data.get('title'), str),
        'year' in data and not isinstance(data.get('year'), int)
    ]):
        abort(400)
    cd = {
        'name': data.get('name', cd['name']),
        'title': data.get('title', cd['title']),
        'year': data.get('year', cd['year'])
    }
    cds.update(cd_id, cd)
    return jsonify({'cd': cd})


if __name__ == "__main__":
    app.run(debug=True)