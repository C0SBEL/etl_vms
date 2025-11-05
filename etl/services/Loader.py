import sqlite3
import json

class Loader:
    def __init__(self, db_path="etl_results.db", reset=False):
        self.db_path = db_path
        self._create_tables()
        if reset:
            self._clear_tables()

    def _clear_tables(self):
        with sqlite3.connect(self.db_path) as conn:
            c = conn.cursor()
            c.execute("DELETE FROM users")
            c.execute("DELETE FROM statistics")
            conn.commit()

    def _create_tables(self):
        with sqlite3.connect(self.db_path) as conn:
            c = conn.cursor()

            c.execute("""
                CREATE TABLE IF NOT EXISTS users (
                    uuid TEXT PRIMARY KEY,
                    gender TEXT,
                    title TEXT,
                    first_name TEXT,
                    last_name TEXT,
                    street_number INTEGER,
                    street_name TEXT,
                    city TEXT,
                    state TEXT,
                    country TEXT,
                    postcode TEXT,
                    latitude REAL,
                    longitude REAL,
                    timezone_offset TEXT,
                    timezone_description TEXT,
                    email TEXT,
                    username TEXT,
                    password TEXT,
                    salt TEXT,
                    md5 TEXT,
                    sha1 TEXT,
                    sha256 TEXT,
                    dob_date TEXT,
                    dob_age INTEGER,
                    registered_date TEXT,
                    registered_age INTEGER,
                    phone TEXT,
                    cell TEXT,
                    id_name TEXT,
                    id_value TEXT,
                    picture_large TEXT,
                    picture_medium TEXT,
                    picture_thumbnail TEXT,
                    nat TEXT
                )
            """)

            c.execute("""
                CREATE TABLE IF NOT EXISTS statistics (
                    total_users INTEGER,
                    avg_registered_age REAL,
                    median_registered_age REAL,
                    stdev_registered_age REAL,
                    min_registered_age REAL,
                    max_registered_age REAL,
                    male_percentage REAL,
                    female_percentage REAL,
                    unique_countries INTEGER,
                    avg_age REAL,
                    stdev_age REAL,
                    min_age REAL,
                    max_age REAL,
                    correlation_age_registered REAL,
                    top_5_ancient TEXT,
                    registration_timeline TEXT,
                    registration_seasonality TEXT,
                    most_common_names TEXT,
                    user_retention TEXT,
                    age_groups TEXT,
                    latest_user TEXT
                )
            """)
            conn.commit()

    def save_users(self, users):
        with sqlite3.connect(self.db_path) as conn:
            c = conn.cursor()
            records = []
            for u in users:
                records.append((
                    u.get("login", {}).get("uuid"),
                    u.get("gender"),
                    u.get("name", {}).get("title"),
                    u.get("name", {}).get("first"),
                    u.get("name", {}).get("last"),
                    u.get("location", {}).get("street", {}).get("number"),
                    u.get("location", {}).get("street", {}).get("name"),
                    u.get("location", {}).get("city"),
                    u.get("location", {}).get("state"),
                    u.get("location", {}).get("country"),
                    str(u.get("location", {}).get("postcode")),
                    float(u.get("location", {}).get("coordinates", {}).get("latitude", 0)),
                    float(u.get("location", {}).get("coordinates", {}).get("longitude", 0)),
                    u.get("location", {}).get("timezone", {}).get("offset"),
                    u.get("location", {}).get("timezone", {}).get("description"),
                    u.get("email"),
                    u.get("login", {}).get("username"),
                    u.get("login", {}).get("password"),
                    u.get("login", {}).get("salt"),
                    u.get("login", {}).get("md5"),
                    u.get("login", {}).get("sha1"),
                    u.get("login", {}).get("sha256"),
                    u.get("dob", {}).get("date"),
                    u.get("dob", {}).get("age"),
                    u.get("registered", {}).get("date"),
                    u.get("registered", {}).get("age"),
                    u.get("phone"),
                    u.get("cell"),
                    u.get("id", {}).get("name"),
                    u.get("id", {}).get("value"),
                    u.get("picture", {}).get("large"),
                    u.get("picture", {}).get("medium"),
                    u.get("picture", {}).get("thumbnail"),
                    u.get("nat")
                ))
            c.executemany(
                """
                INSERT OR REPLACE INTO users (
                    uuid, gender, title, first_name, last_name, street_number, street_name,
                    city, state, country, postcode, latitude, longitude, timezone_offset, timezone_description,
                    email, username, password, salt, md5, sha1, sha256, dob_date, dob_age,
                    registered_date, registered_age, phone, cell, id_name, id_value,
                    picture_large, picture_medium, picture_thumbnail, nat
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                records
            )
            conn.commit()
            print(f"{len(users)} usuarios guardados en la base de datos.")

    def save_statistics(self, stats):
        """Guarda las estadísticas completas en la tabla 'statistics'."""
        with sqlite3.connect(self.db_path) as conn:
            c = conn.cursor()
            c.execute("DELETE FROM statistics")

            # Insertar los datos (usamos json.dumps para estructuras complejas)
            c.execute("""
                INSERT INTO statistics (
                    total_users, avg_registered_age, median_registered_age, stdev_registered_age,
                    min_registered_age, max_registered_age, male_percentage, female_percentage,
                    unique_countries, avg_age, stdev_age, min_age, max_age,
                    correlation_age_registered, top_5_ancient, registration_timeline,
                    registration_seasonality, most_common_names, user_retention,
                    age_groups, latest_user
                )
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                stats.get("total_users"),
                stats.get("years_registered_stats", {}).get("average"),
                stats.get("years_registered_stats", {}).get("median"),
                stats.get("years_registered_stats", {}).get("stdev"),
                stats.get("years_registered_stats", {}).get("min"),
                stats.get("years_registered_stats", {}).get("max"),
                stats.get("gender_distribution", {}).get("male"),
                stats.get("gender_distribution", {}).get("female"),
                stats.get("unique_countries"),
                stats.get("age_distribution", {}).get("average"),
                stats.get("age_distribution", {}).get("stdev"),
                stats.get("age_distribution", {}).get("min"),
                stats.get("age_distribution", {}).get("max"),
                stats.get("age_registered_correlation"),
                json.dumps(stats.get("top_5_ancient")),
                json.dumps(stats.get("registration_timeline")),
                json.dumps(stats.get("registration_seasonality")),
                json.dumps(stats.get("most_common_names")),
                json.dumps(stats.get("user_retention_analysis")),
                json.dumps(stats.get("age_groups_distribution")),
                json.dumps(stats.get("latest_user"))
            ))
            conn.commit()
            print("Estadísticas guardadas correctamente.")
