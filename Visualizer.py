import os
import matplotlib.pyplot as plt
import geopandas as gpd

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

    def plot_country_choropleth(self, country_dist):
        if not country_dist:
            print("No hay datos de países para generar el mapa.")
            return

        world = gpd.read_file("https://naturalearth.s3.amazonaws.com/110m_cultural/ne_110m_admin_0_countries.zip")
        world["percentage"] = world["NAME"].map(country_dist).fillna(0)

        fig, ax = plt.subplots(figsize=(15, 8))
        world.plot(
            column="percentage",
            cmap="Blues",
            linewidth=0.5,
            edgecolor="black",
            legend=True,
            ax=ax
        )

        plt.title("Mapa mundial: Distribución de usuarios por país (%)", fontsize=14, weight="bold", pad=20)

        path = os.path.join(self.output_dir, "country_choropleth.png")
        plt.tight_layout()
        plt.savefig(path, dpi=300)
        plt.close()
        print(f"Mapa guardado en: {path}")

    def generate_visualizations(self, users, stats):
        if not users:
            print("⚠️ No se proporcionaron usuarios para la visualización.")
            return

        self.users = users
        self.stats = stats

        # Llamar a los métodos de visualización
        self.plot_gender_distribution()
        self.plot_time_registered_distribution()

        country_dist = self.stats.get("country_distribution")
        if country_dist:
            self.plot_country_choropleth(country_dist)
        else:
            print("No hay distribución de países en las estadísticas.")


