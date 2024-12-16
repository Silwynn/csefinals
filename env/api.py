from flask import Flask, make_response, jsonify, request
from flask_mysqldb import MySQL

app = Flask(__name__)

# MySQL configuration
app.config["MYSQL_HOST"] = "127.0.0.1"
app.config["MYSQL_USER"] = "root"
app.config["MYSQL_PASSWORD"] = ""
app.config["MYSQL_DB"] = "CSE"
app.config["MYSQL_CURSORCLASS"] = "Cursor"

mysql = MySQL(app)

# Helper functions for fetching and inserting data
def data_fetch(query, params=None):
    cur = mysql.connection.cursor()
    cur.execute(query, params)
    data = cur.fetchall()
    cur.close()
    return data


def data_insert(query, params=None):
    cur = mysql.connection.cursor()
    cur.execute(query, params)
    mysql.connection.commit()
    rows_affected = cur.rowcount
    cur.close()
    return rows_affected


# Route for adding gender
@app.route('/gender', methods=['POST'])
def add_gender():
    info = request.get_json()
    gender_code = info.get("gender_code")
    gender_description = info.get("gender_description")
    if not gender_code or not gender_description:
        return make_response(jsonify({"error": "Missing required fields"}), 400)
    rows_affected = data_insert(
        "INSERT INTO gender (gender_code, gender_description) VALUES (%s, %s)",
        (gender_code, gender_description)
    )
    return make_response(jsonify({"message": "Gender added", "rows_affected": rows_affected}), 201)


# Route for adding club
@app.route('/club', methods=['POST'])
def add_club():
    info = request.get_json()
    club_id = info.get("club_id")
    club_name = info.get("club_name")
    club_location = info.get("club_location")
    if not club_id or not club_name or not club_location:
        return make_response(jsonify({"error": "Missing required fields"}), 400)
    rows_affected = data_insert(
        "INSERT INTO club (club_id, club_name, club_location) VALUES (%s, %s, %s)",
        (club_id, club_name, club_location)
    )
    return make_response(jsonify({"message": "Club added", "rows_affected": rows_affected}), 201)


# Route for adding category
@app.route('/category', methods=['POST'])
def add_category():
    info = request.get_json()
    category_code = info.get("category_code")
    category_description = info.get("category_description")
    if not category_code or not category_description:
        return make_response(jsonify({"error": "Missing required fields"}), 400)
    rows_affected = data_insert(
        "INSERT INTO category (category_code, category_description) VALUES (%s, %s)",
        (category_code, category_description)
    )
    return make_response(jsonify({"message": "Category added", "rows_affected": rows_affected}), 201)


# Route for adding athlete (denormalized version)
@app.route('/athlete', methods=['POST'])
def add_athlete():
    info = request.get_json()
    athlete_id = info.get("athlete_id")
    athlete_firstname = info.get("athlete_firstname")
    athlete_surname = info.get("athlete_surname")
    athlete_other_details = info.get("athlete_other_details")
    gender_code = info.get("gender_code")
    gender_description = info.get("gender_description")
    club_id = info.get("club_id")
    club_name = info.get("club_name")
    club_location = info.get("club_location")
    category_code = info.get("category_code")
    category_description = info.get("category_description")
    
    # Ensure required fields are provided
    if not all([athlete_id, athlete_firstname, athlete_surname, gender_code, gender_description, club_id, club_name, club_location, category_code, category_description]):
        return make_response(jsonify({"error": "Missing required fields"}), 400)
    
    rows_affected = data_insert(
        """INSERT INTO athletes_info (athlete_id, athlete_firstname, athlete_surname, athlete_other_details, gender_code, gender_description, 
           club_id, club_name, club_location, category_code, category_description)
           VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)""",
        (athlete_id, athlete_firstname, athlete_surname, athlete_other_details, gender_code, gender_description, 
         club_id, club_name, club_location, category_code, category_description)
    )
    return make_response(jsonify({"message": "Athlete added", "rows_affected": rows_affected}), 201)


if __name__ == "__main__":
    app.run(debug=True)
