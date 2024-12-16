from flask import Flask
from flask_mysqldb import MySQL
from faker import Faker
import random
import MySQLdb  # For MySQLdb exceptions

app = Flask(__name__)

# Database Configuration
app.config["MYSQL_HOST"] = "127.0.0.1"
app.config["MYSQL_USER"] = "root"
app.config["MYSQL_PASSWORD"] = "root"
app.config["MYSQL_DB"] = "athletes_and_events"
app.config["MYSQL_CURSORCLASS"] = "DictCursor"

mysql = MySQL(app)

# Use Filipino-specific faker locale for authentic names and places
fake = Faker('en_PH')

def generate_genders():
    return [
        {'gender_code': 'M', 'gender_description': 'Male'},
        {'gender_code': 'F', 'gender_description': 'Female'}
    ]

def generate_clubs():
    clubs = []
    for i in range(1, 26):  # Generate 25 clubs
        club = {
            'club_name': fake.company(),
            'club_location': fake.city()
        }
        clubs.append(club)
    return clubs

def generate_athletes():
    athletes = []
    for i in range(1, 26):  # Generate 25 athletes
        athlete = {
            'athlete_firstname': fake.first_name(),
            'athlete_surname': fake.last_name(),
            'athlete_other_details': fake.text(max_nb_chars=200),
            'gender_code': random.choice(['M', 'F']),
            'club_id': random.randint(1, 25)  # Assumes 25 clubs exist
        }
        athletes.append(athlete)
    return athletes

def generate_categories():
    categories = []
    for i in range(26):  
        category = {
            'category_code': chr(65 + i),  
            'category_description': fake.text(max_nb_chars=50)
        }
        categories.append(category)
    return categories

def generate_event_types():
    event_types = []
    for i in range(1, 26):  # Generate 25 event types
        event_type = {
            'event_type_code': chr(65 + i % 26),  # Generate A-Z cyclically
            'event_type_description': fake.text(max_nb_chars=50)
        }
        event_types.append(event_type)
    return event_types

def generate_event_series():
    event_series = []
    for i in range(1, 26):  # Generate 25 event series
        series = {
            'series_number': i,
            'series_date_time': fake.date_time_this_year(),
            'series_name': fake.sentence(nb_words=2)
        }
        event_series.append(series)
    return event_series

def generate_events():
    events = []
    for i in range(1, 26):  # Generate 25 events
        event = {
            'event_id': i,
            'event_date': fake.date_this_year(),
            'event_name': fake.sentence(nb_words=3),
            'event_distance': round(random.uniform(1.0, 42.2), 2),
            'event_other_details': fake.text(max_nb_chars=200),
            'category_code': random.choice([chr(65 + i) for i in range(26)]),
            'event_type_code': random.choice([chr(65 + i) for i in range(26)]),
            'series_number': random.randint(1, 25)
        }
        events.append(event)
    return events

def insert_data():
    db_connection = mysql.connection
    cursor = db_connection.cursor()
    try:
        # Insert Categories
        categories = generate_categories()
        for category in categories:
            print(f"Inserting category: {category}")
            cursor.execute("""
                INSERT INTO category (category_code, category_description) 
                VALUES (%s, %s)
                ON DUPLICATE KEY UPDATE category_description = VALUES(category_description)
            """, (category['category_code'], category['category_description']))

        # Insert Event Types
        event_types = generate_event_types()
        for event_type in event_types:
            print(f"Inserting event type: {event_type}")
            cursor.execute("""
                INSERT INTO event_type (event_type_code, event_type_description) 
                VALUES (%s, %s)
                ON DUPLICATE KEY UPDATE event_type_description = VALUES(event_type_description)
            """, (event_type['event_type_code'], event_type['event_type_description']))

        # Insert Event Series
        event_series = generate_event_series()
        for series in event_series:
            print(f"Inserting event series: {series}")
            cursor.execute("""
                INSERT INTO event_series (series_number, series_date_time, series_name) 
                VALUES (%s, %s, %s)
            """, (series['series_number'], series['series_date_time'], series['series_name']))

        # Insert Events
        events = generate_events()
        for event in events:
            print(f"Inserting event: {event}")
            cursor.execute("""
                INSERT INTO event (event_id, event_date, event_name, event_distance, event_other_details, category_code, event_type_code, series_number) 
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            """, (event['event_id'], event['event_date'], event['event_name'], event['event_distance'], event['event_other_details'], event['category_code'], event['event_type_code'], event['series_number']))
        
        db_connection.commit()
    except Exception as e:
        db_connection.rollback()
        print(f"Error during data insertion: {e}")
    finally:
        cursor.close()

@app.route('/generate_data', methods=['GET'])
def generate_data():
    insert_data()
    return "Fake data inserted successfully!"

if __name__ == "__main__":
    app.run(debug=True)
