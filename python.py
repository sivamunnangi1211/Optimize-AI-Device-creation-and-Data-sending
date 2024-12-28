from flask import Flask, request, jsonify

app = Flask(__name__)

# Initialize a global list to store tags data
tags_data = []

@app.route('/')
def home():
    return "Welcome to the Flask application!"

@app.route('/plodder1', methods=['POST'])
def handle_plodder1():
    data = request.json
    print("end point data:", data)
    reader_name = data.get('reader_name')
    print(reader_name)
    
    if data and isinstance(data.get('event_data'), list):
        for event in data['event_data']:
            if 'ep' in event and reader_name:
                tag_name = event['ep']
                if tag_name not in tags_data:  # Check if tag has not been added before
                    tags_data.append(tag_name)
                    print(tags_data)
        # db.session.commit()  # Uncomment this if you have a database session to commit
        return jsonify({'tags_data': tags_data, 'reader_name': reader_name})
    
    return jsonify({'error': 'No valid data provided'})

# Optional: Add a route to handle favicon requests
@app.route('/favicon.ico')
def favicon():
    return '', 204

if __name__ == '__main__':
    app.run(debug=True)
