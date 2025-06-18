from flask import Flask, render_template, request, redirect, url_for, jsonify
from pymongo import MongoClient
import json

app = Flask(__name__)

# MongoDB Atlas connection
client = MongoClient("your_mongodb_connection_string")
db = client['MyDatabase']
collection = db['Submissions']

@app.route('/')
def index():
    return render_template('todo.html')

@app.route('/submit', methods=['POST'])
def submit():
    name = request.form.get('name')
    email = request.form.get('email')
    try:
        #collection.insert_one({"name": name, "email": email})
        return redirect(url_for('success'))
    except Exception as e:
        return render_template('form.html', error=str(e))

@app.route('/submittodoitem', methods=['POST'])
def submit_todo():
    item_name = request.form.get('itemName')
    item_description = request.form.get('itemDescription')
    
    if not item_name or not item_description:
        return "Missing fields", 400

    collection.insert_one({
        "itemName": item_name,
        "itemDescription": item_description
    })

    return "To-Do Item Submitted Successfully"

@app.route('/success')
def success():
    return "Data submitted successfully"

@app.route('/api')
def get_data():
    with open('data.json') as f:
        data = json.load(f)
    return jsonify(data)

if __name__ == '__main__':
    app.run(debug=True)
