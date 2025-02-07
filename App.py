from flask import Flask, request, jsonify,Response
from flask_cors import CORS
import sqlite3
import logging
import csv
import io


# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


app = Flask(__name__)
CORS(app)


DATABASE = 'clicks.db'


def init_db():
    try:
        conn = sqlite3.connect(DATABASE)
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS clicks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                x INTEGER NOT NULL,
                y INTEGER NOT NULL,
                value INTEGER NOT NULL,
                timestamp TEXT NOT NULL
            )
        ''')
        conn.commit()
        conn.close()
        logger.info("Database initialized successfully")
    except Exception as e:
        logger.error(f"Database initialization error: {str(e)}")


init_db()


@app.route('/api/clicks', methods=['POST'])
def save_click():
    try:
        data = request.get_json()
        logger.debug(f"Received data: {data}")  # Log received data
       
        # Validate data
        required_fields = ['x', 'y', 'value', 'timestamp']
        if not all(field in data for field in required_fields):
            missing_fields = [field for field in required_fields if field not in data]
            return jsonify({
                'error': 'Missing required fields',
                'missing_fields': missing_fields
            }), 400


        conn = sqlite3.connect(DATABASE)
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO clicks (x, y, value, timestamp)
            VALUES (?, ?, ?, ?)
        ''', (data['x'], data['y'], data['value'], data['timestamp']))
        conn.commit()
        conn.close()
       
        logger.info(f"Successfully saved click data: {data}")
        return jsonify({'message': 'Click saved successfully!'}), 201
       
    except Exception as e:
        logger.error(f"Error saving click: {str(e)}")
        return jsonify({'error': str(e)}), 500


@app.route('/api/clicks', methods=['GET'])
def get_clicks():
    try:
        conn = sqlite3.connect(DATABASE)
        cursor = conn.cursor()
        cursor.execute('SELECT x, y, value, timestamp FROM clicks')
        clicks = cursor.fetchall()
        conn.close()


        results = [
            {'x': row[0], 'y': row[1], 'value': row[2], 'timestamp': row[3]}
            for row in clicks
        ]
        return jsonify(results), 200
    except Exception as e:
        logger.error(f"Error retrieving clicks: {str(e)}")
        return jsonify({'error': str(e)}), 500
    
@app.route('/api/clicks/csv', methods=['GET'])
def get_clicks_csv():
    try:
        conn = sqlite3.connect(DATABASE)
        cursor = conn.cursor()
        cursor.execute('SELECT x, y, value, timestamp FROM clicks')
        clicks = cursor.fetchall()
        conn.close()

        
        file = io.StringIO()
        writer = csv.writer(file)
        writer.writerow(['x', 'y', 'value', 'timestamp'])
        for row in clicks:
            writer.writerow(row)
        file.seek(0)

        return Response(
            file,
            mimetype="text/csv",
            headers={"Content-Disposition": "attachment;filename=output.csv"}
        )

    except Exception as e:
        logger.error(f"Error generating CSV file: {str(e)}")
        return jsonify({'error': str(e)}), 500
    
@app.route('/api/clicks/stats', methods=['GET'])
def get_click_stats():
    try:
        conn = sqlite3.connect(DATABASE)
        cursor = conn.cursor()
        cursor.execute('''
            SELECT DATE(timestamp) AS date, COUNT(*) AS count
            FROM clicks
            GROUP BY DATE(timestamp)
            ORDER BY DATE(timestamp) DESC
        ''')
        rows = cursor.fetchall()
        conn.close()
        return jsonify([{"date": row[0], "count": row[1]} for row in rows]),200
    except Exception as e:
        logger.error(f"Error retrieving click stats: {str(e)}")
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=50000)
