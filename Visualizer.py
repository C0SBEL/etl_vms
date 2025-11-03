import os
import matplotlib.pyplot as plt
import simplekml
import statistics

class Visualizer:
    def __init__(self, output_dir="visualizations", clean=True):
        self.users = []
        self.stats = {}
        self.output_dir = output_dir
        os.makedirs(self.output_dir, exist_ok=True)

        if clean:
            self._clean_directory()

    def _clean_directory(self):
        for filename in os.listdir(self.output_dir):
            file_path = os.path.join(self.output_dir, filename)
            try:
                if os.path.isfile(file_path) or os.path.islink(file_path):
                    os.unlink(file_path)
                elif os.path.isdir(file_path):
                    import shutil
                    shutil.rmtree(file_path)
            except Exception as e:
                print(f"⚠️ No se pudo eliminar {file_path}: {e}")

    def plot_gender_distribution(self):
        genders = [u.get("gender") for u in self.users if "gender" in u]
        total = len(genders)
        if total == 0:
            print("⚠️ No hay datos de género.")
            return

        gender_dist = self.stats.get("gender_distribution")
        if not gender_dist:
            print("⚠️ No hay estadísticas de género en stats.")
            return

        plt.figure(figsize=(8, 6))
        bars = plt.bar(gender_dist.keys(), gender_dist.values(), color=["skyblue", "darksalmon"])
        plt.ylabel("Porcentaje (%)")
        plt.title("Distribución de género")

        for bar, value in zip(bars, gender_dist.values()):
            plt.text(bar.get_x() + bar.get_width() / 2, value + 0.5, f"{value}%", ha="center", va="bottom")

        plt.tight_layout()
        path = os.path.join(self.output_dir, "gender_distribution.png")
        plt.savefig(path)
        plt.close()

    def plot_time_registered_distribution(self):
        times = [u["registered"]["age"] for u in self.users if "registered" in u and "age" in u["registered"]]
        if not times:
            print("⚠️ No hay datos de tiempo registrado.")
            return

        avg_time = self.stats.get("average_time_registered")
        if avg_time is None:
            print("⚠️ No hay estadística de tiempo registrado promedio.")

        # Crear histograma
        plt.figure(figsize=(8, 5))
        plt.hist(times, bins=10, color="skyblue", edgecolor="black")
        plt.xlabel("Años registrados")
        plt.ylabel("Número de usuarios")
        plt.title("Distribución del tiempo que los usuarios llevan registrados")

        # Línea de referencia de la media
        plt.axvline(avg_time, color="red", linestyle="dashed", linewidth=2)
        plt.text(avg_time + 0.1, plt.ylim()[1] * 0.9, f"Media = {avg_time} años", color="red")

        # Guardar gráfico
        path = os.path.join(self.output_dir, "registered_time_distribution.png")
        plt.tight_layout()
        plt.savefig(path)
        plt.close()

    def plot_user_locations(self):
        kml = simplekml.Kml()

        for u in self.users:
            try:
                location = u["location"]
                coords = location["coordinates"]
                lat = coords["latitude"]
                lon = coords["longitude"]

                name = f"{u['name']['first']} {u['name']['last']}"
                kml.newpoint(name=name, coords=[(lon, lat)])

            except KeyError:
                continue

        path = os.path.join(self.output_dir, "user_locations.kml")
        kml.save(path)
        print(f"✅ KML created: {path}")


def avg_by_country(self, top_n: int=10):
    valid_users = [u for u in self.users if "location" in u and "country" in u["location"] and "dob" in u and "age" in u["dob"]]

    country_ages = {}

    for u in valid_users:
        country = u["location"]["country"]
        age = u["dob"]["age"]
        country_ages.setdefault(country, []).append(age)

    avg_by_country = {country: round(statistics.mean(ages), 1) for country, ages in country_ages.items() if ages}

    ordered_countries = sorted(
        avg_by_country.items(),
        key=lambda item: item[1],
        reverse=True
    )

    top_countries = ordered_countries[:top_n]

    data = self.avg_by_country(top_n=top_n)
    if not data:
        print("⚠️ No hi ha dades per països.")
        return

    countries = [d["country"] for d in data]
    values = [d["avg_age"] for d in data]

    plt.figure(figsize=(10, 6))
    bars = plt.bar(countries, values, color="steelblue")

    plt.title(f"Mitjana d’edat per país (Top {top_n})")
    plt.ylabel("Edat mitjana")
    plt.xlabel("País")
    plt.xticks(rotation=45, ha="right")

    for bar, val in zip(bars, values):
        plt.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 0.3, f"{val}", ha="center", va="bottom")

    plt.tight_layout()
    path = os.path.join(self.output_dir, "avg_age_by_country.png")
    plt.savefig(path)
    plt.close()
    print(f"✅ Gràfic guardat: {path}")



    def generate_visualizations(self, users, stats):
        if users:
            self.users = users
        else:
            print("⚠️ No se proporcionaron usuarios para la visualización.")
            return

        self.stats = stats

        # Llamar a los métodos de visualización

        self.plot_gender_distribution()
        self.plot_time_registered_distribution()
        self.plot_user_locations()
        self.plot_user_locations()
        self.avg_by_country()
