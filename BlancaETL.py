#EXTRACTOR
import requests
import csv
url="https://randomuser.me/api/?results=5000"
csv_file = "/Users/blancagallardo/Downloads/simplemaps_worldcities_basicv1.901/worldcities.csv"

def get_users():
    try:
        response = requests.get(url)
        if response.status_code ==200:
            data = response.json()
            print("5000 datos de usuarios obtenidos correctamente en formato JSON")
            return data.get("results", [])
        else:
            print("Error al obtener los datos")
            return []
    except Exception as e:
        print("Error al hacer la petición:", e)
        return []
def load_city_country(csv_file):
    city_country = {}
    try:
        with open(csv_file, encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                city = row.get("city")
                country = row.get("country")
                if city and country:
                    city_country[city.lower()] = country.lower()
        print(f"Diccionario de ciudades cargado con {len(city_country)} entradas.")
    except FileNotFoundError:
        print(f"El archivo CSV no se encontró en: {csv_file}")
    except Exception as e:
        print(f"Error al leer el archivo CSV: {e}")
    return city_country
#TRANSFORMER (DATA CLEANER)
def clean_user(users, city_country):
        user_clean = []
        for user in users :
            if not user:
                continue
            age = user["dob"]["age"]
            if age < 18 or age > 115:
                continue
            city = user["location"]["city"]
            country = user["location"]["country"]
            if city in city_country:
                if city_country[city] != country:
                    continue
            user_clean.append(user)
        return user_clean
#TRANSFORMER (ESTADISTICA)

#CONTROLER
if __name__ == "__main__":
    users = get_users()
    city_country = load_city_country(csv_file)
    print(f"Registros totales antes de limpiar: {len(users)}")
    users_clean = clean_user(users, city_country)
    print(f"Registros después de limpiar: {len(users_clean)}")
