from flask import Flask, request, jsonify
from flask_cors import CORS
from pymongo import MongoClient, errors
from flasgger import Swagger
import logging
from flask_jwt_extended import (
    JWTManager, create_access_token, jwt_required, get_jwt_identity
)

app = Flask(__name__)
CORS(app)  # Allow cross-origin requests
swagger = Swagger(app)

# Configure logging with log level and format
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

# Configure JWT
app.config["JWT_SECRET_KEY"] = "super-secret-key"  # Use a more complex key in production
jwt = JWTManager(app)

# Connect to MongoDB (ensure MongoDB service is running)
try:
    client = MongoClient("mongodb://127.0.0.1:27017/", serverSelectionTimeoutMS=5000)
    client.server_info()  # Check connection
    db = client["professor_dashboard"]  # Database name
    professors_collection = db["professors"]  # Collection name
    logging.info("Connected to MongoDB successfully.")
except errors.ServerSelectionTimeoutError as err:
    logging.error("Failed to connect to MongoDB: %s", err)
    raise err

# Initialize data: If the collection is empty, insert some initial data (optional)
if professors_collection.count_documents({}) == 0:
    initial_data = [
        {"id": 1, "name": "Dr. Smith", "title": "Professor", "department": "Computer Science"},
        {"id": 2, "name": "Dr. Johnson", "title": "Associate Professor", "department": "Mathematics"}
    ]
    professors_collection.insert_many(initial_data)
    logging.info("Inserted initial data into MongoDB.")

# ---------------------------
# User Authentication Endpoints
# ---------------------------

@app.route('/login', methods=['POST'])
def login():
    """
    User login to obtain access token (JWT)
    ---
    parameters:
      - in: body
        name: credentials
        description: Username and password
        schema:
          type: object
          required:
            - username
            - password
          properties:
            username:
              type: string
            password:
              type: string
    responses:
      200:
        description: Login successful, returns JWT token
        schema:
          type: object
          properties:
            access_token:
              type: string
      401:
        description: Invalid username or password
    """
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")
    
    # Using simple authentication logic here; in a real project, query the database to validate user info.
    if username != "admin" or password != "password":
        logging.warning("Login failed, invalid username or password: %s", username)
        return jsonify({"msg": "Bad username or password"}), 401

    access_token = create_access_token(identity=username)
    logging.info("User %s logged in successfully", username)
    return jsonify(access_token=access_token), 200

@app.route('/protected', methods=['GET'])
@jwt_required()
def protected():
    """
    Protected endpoint, only accessible with a valid JWT
    ---
    responses:
      200:
        description: Returns current logged-in user information
        schema:
          type: object
          properties:
            logged_in_as:
              type: string
    """
    current_user = get_jwt_identity()
    logging.info("Protected endpoint accessed by user: %s", current_user)
    return jsonify(logged_in_as=current_user), 200

# ---------------------------
# Professor CRUD Endpoints
# ---------------------------

@app.route('/', methods=['GET'])
def index():
    """
    Welcome endpoint
    ---
    responses:
      200:
        description: Welcome message
    """
    return "Welcome to the Professor Dashboard API!"

@app.route('/professors', methods=['GET'])
def get_professors():
    """
    Retrieve all professor data
    ---
    responses:
      200:
        description: Returns all professor data
        schema:
          type: array
          items:
            type: object
    """
    try:
        professors = list(professors_collection.find({}, {"_id": 0}))
        logging.info("Successfully fetched professor data.")
        return jsonify(professors), 200
    except Exception as e:
        logging.error("Error fetching professor data: %s", e)
        return jsonify({"error": "Failed to fetch professor data"}), 500

@app.route('/professors', methods=['POST'])
@jwt_required()  # Protected endpoint, only logged in users can add a professor
def add_professor():
    """
    Add a new professor
    ---
    parameters:
      - in: body
        name: professor
        description: Professor data
        schema:
          type: object
          required:
            - name
            - title
            - department
          properties:
            name:
              type: string
            title:
              type: string
            department:
              type: string
    responses:
      201:
        description: Returns the newly added professor data
    """
    try:
        # Attempt to get data in JSON format
        new_prof = request.get_json()
        # If JSON is not available, try to get data from form
        if not new_prof:
            new_prof = request.form.to_dict()
        if not new_prof:
            return jsonify({"error": "No data provided"}), 400

        # Generate new ID
        max_prof = professors_collection.find_one(sort=[("id", -1)])
        new_id = max_prof["id"] + 1 if max_prof and "id" in max_prof else 1
        new_prof["id"] = new_id

        result = professors_collection.insert_one(new_prof)
        inserted_prof = professors_collection.find_one({"_id": result.inserted_id}, {"_id": 0})
        logging.info("Added new professor: %s", inserted_prof)
        return jsonify(inserted_prof), 201
    except Exception as e:
        logging.error("Error adding professor: %s", e)
        return jsonify({"error": "Failed to add professor"}), 500

@app.route('/professors/<int:prof_id>', methods=['PUT'])
@jwt_required()  # Protected endpoint, requires login
def update_professor(prof_id):
    """
    Update specified professor data
    ---
    parameters:
      - name: prof_id
        in: path
        type: integer
        required: true
        description: Professor ID
      - in: body
        name: professor
        description: Data to update
        schema:
          type: object
          properties:
            name:
              type: string
            title:
              type: string
            department:
              type: string
    responses:
      200:
        description: Returns the updated professor data
      404:
        description: Professor not found
    """
    try:
        update_data = request.get_json()
        if not update_data:
            return jsonify({"error": "No update data provided"}), 400

        result = professors_collection.update_one({"id": prof_id}, {"$set": update_data})
        if result.matched_count == 0:
            return jsonify({"error": "Professor not found"}), 404

        updated_prof = professors_collection.find_one({"id": prof_id}, {"_id": 0})
        logging.info("Updated professor id %s: %s", prof_id, updated_prof)
        return jsonify(updated_prof), 200
    except Exception as e:
        logging.error("Error updating professor: %s", e)
        return jsonify({"error": "Failed to update professor"}), 500

@app.route('/professors/<int:prof_id>', methods=['DELETE'])
@jwt_required()  # Protected endpoint, requires login
def delete_professor(prof_id):
    """
    Delete specified professor data
    ---
    parameters:
      - name: prof_id
        in: path
        type: integer
        required: true
        description: Professor ID
    responses:
      200:
        description: Returns a success indicator for deletion
      404:
        description: Professor not found
    """
    try:
        result = professors_collection.delete_one({"id": prof_id})
        if result.deleted_count == 0:
            return jsonify({"error": "Professor not found"}), 404
        logging.info("Deleted professor id %s", prof_id)
        return jsonify({"success": True}), 200
    except Exception as e:
        logging.error("Error deleting professor: %s", e)
        return jsonify({"error": "Failed to delete professor"}), 500

if __name__ == '__main__':
    app.run(debug=True)
