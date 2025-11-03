import sqlite3

class Loader:
    def __init__(self, db_path="etl_results.db", reset=False):
        self.db_path = db_path
        self._create_tables()
        if reset:
            self._clear_tables()

    def _clear_tables(self):
        """Vacía las tablas de la base de datos."""
        with sqlite3.connect(self.db_path) as conn:
            c = conn.cursor()
            c.execute("DELETE FROM users")
            c.execute("DELETE FROM statistics")
            conn.commit()

    def _create_tables(self):
        """Crea las tablas si no existen."""
        with sqlite3.connect(self.db_path) as conn:
            c = conn.cursor()
            # Tabla de usuarios con todos los campos relevantes
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
            # Tabla de estadísticas
            c.execute("""
                CREATE TABLE IF NOT EXISTS statistics (
                    total_users INTEGER,
                    avg_registered_age REAL,
                    male_percentage REAL,
                    female_percentage REAL
                )
            """)
            conn.commit()

    def save_users(self, users):
        """Guarda los usuarios en la tabla 'users'."""
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
                    str(u.get("location", {}).get("postcode")),  # puede ser string o int
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
            print(f"💾 {len(users)} usuarios guardados en la base de datos.")

    def save_statistics(self, stats):
        """Guarda las estadísticas en la tabla 'statistics'."""
        with sqlite3.connect(self.db_path) as conn:
            c = conn.cursor()
            c.execute("DELETE FROM statistics")
            c.execute(
                """
                INSERT INTO statistics (total_users, avg_registered_age, male_percentage, female_percentage)
                VALUES (?, ?, ?, ?)
                """,
                (
                    stats["total_users"],
                    stats["average_time_registered"],
                    stats["gender_distribution"]["male"],
                    stats["gender_distribution"]["female"]
                )
            )
            conn.commit()
            print("💾 Estadísticas guardadas correctamente.")
