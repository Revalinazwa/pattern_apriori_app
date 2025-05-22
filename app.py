# app.py
from flask import Flask, request, jsonify
from flask_cors import CORS
from apriori_logic import apriori_model
from dataset_storage import get_dataset, add_transaction, update_transaction, delete_transaction

app = Flask(__name__)
CORS(app)

@app.route('/', methods=['GET'])
def home():
    return jsonify({'message': 'Flask API Apriori Tajwid is running!'}), 200

@app.route('/dataset', methods=['POST'])
def add_data():
    data = request.json
    if not isinstance(data, list):
        return jsonify({'error': 'Input harus list hukum tajwid'}), 400
    add_transaction(data)
    return jsonify({'message': 'Transaksi ditambahkan'}), 200

@app.route('/dataset', methods=['GET'])
def view_dataset():
    return jsonify(get_dataset())

@app.route('/dataset/<int:index>', methods=['DELETE'])
def delete_data(index):
    if delete_transaction(index):
        return jsonify({'message': 'Transaksi dihapus'}), 200
    return jsonify({'error': 'Index tidak ditemukan'}), 404

@app.route('/dataset/<int:index>', methods=['PUT'])
def update_dataset(index):
    data = request.get_json()
    if 0 <= index < len(dataset):
        dataset[index] = data
        return jsonify({'message': 'Updated'}), 200
    return jsonify({'error': 'Index out of range'}), 404

@app.route('/rules', methods=['POST'])
def generate_rules():
    req = request.json
    min_support = req.get("min_support", 0.3)
    min_confidence = req.get("min_confidence", 0.6)
    dataset = get_dataset()
    if not dataset:
        return jsonify({'error': 'Dataset kosong'}), 400
    rules_df = apriori_model(dataset, min_support, min_confidence)
    rules = rules_df.to_dict(orient='records')
    for rule in rules:
        rule['antecedents'] = list(rule['antecedents'])
        rule['consequents'] = list(rule['consequents'])
    return jsonify(rules), 200

if __name__ == '__main__':
    app.run(debug=True)
