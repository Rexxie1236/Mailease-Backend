from flask import Flask, jsonify, request
import os
from pymongo import MongoClient
import firebase_admin
from firebase_admin import credentials, auth, firestore

app = Flask(__name__)

# **MongoDB Configuration**
mongo_uri = "mongodb+srv://jamesrex1236:jamesrex1236@mail-ease.7l3rq.mongodb.net/Mail-Ease_db?retryWrites=true&w=majority"
client = MongoClient(mongo_uri)

# Access MongoDB collections
db = client["Mail-Ease_db"]
users_collection = db["users"]
emails_collection = db["emails"]

# **Firebase Configuration**
# Load Firebase service account from JSON file
cred = credentials.Certificate("serviceAccount.json")
firebase_admin.initialize_app(cred)

# Access Firebase Firestore
firebase_db = firestore.client()

# **API Endpoints**
@app.route("/", methods=["GET"])
def home():
    return jsonify({"message": "MailEase Backend is Running!"})

@app.route("/add-user", methods=["POST"])
def add_user():
    # Add user to MongoDB
    data = request.json
    if not data or not data.get("email"):
        return jsonify({"error": "Email is required"}), 400

    users_collection.insert_one({
        "name": data.get("name"),
        "email": data.get("email"),
        "password": data.get("password")
    })
    return jsonify({"message": "User added successfully!"})

@app.route("/get-users", methods=["GET"])
def get_users():
    # Fetch all users from MongoDB
    users = list(users_collection.find({}, {"_id": 0}))  # Exclude MongoDB ObjectID
    return jsonify({"users": users})

@app.route("/firebase-users", methods=["GET"])
def get_firebase_users():
    # Fetch all users from Firebase Authentication
    firebase_users = auth.list_users().iterate_all()
    user_list = [{"uid": user.uid, "email": user.email} for user in firebase_users]
    return jsonify({"firebase_users": user_list})

@app.route("/add-email", methods=["POST"])
def add_email():
    # Add email to MongoDB
    data = request.json
    if not data or not data.get("recipient") or not data.get("subject"):
        return jsonify({"error": "Recipient and Subject are required"}), 400

    emails_collection.insert_one({
        "sender": data.get("sender"),
        "recipient": data.get("recipient"),
        "subject": data.get("subject"),
        "body": data.get("body"),
        "timestamp": data.get("timestamp")
    })
    return jsonify({"message": "Email added successfully!"})

@app.route("/get-emails", methods=["GET"])
def get_emails():
    # Fetch all emails from MongoDB
    emails = list(emails_collection.find({}, {"_id": 0}))  # Exclude MongoDB ObjectID
    return jsonify({"emails": emails})

if __name__ == "__main__":
    app.run(debug=True)
