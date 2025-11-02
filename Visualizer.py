import os
import matplotlib.pyplot as plt

class Visualizer:
    def __init__(self, output_dir="visualizations", clean=True):
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

    def plot_gender_distribution(self, gender_distribution):
        if not gender_distribution:
            print("⚠️ No hay datos de género para graficar.")
            return

        plt.bar(gender_distribution.keys(), gender_distribution.values(), color=["skyblue", "lightpink"])
        plt.ylabel("Porcentaje (%)")
        plt.title("Distribución de género")
        plt.tight_layout()
        path = os.path.join(self.output_dir, "gender_distribution.png")
        plt.savefig(path)
        plt.close()
        print(f"📊 Gráfico guardado en: {path}")

    def plot_registered_age(self, avg_age):
        if avg_age is None:
            print("⚠️ No hay edad promedio para graficar.")
            return

        plt.figure(figsize=(4, 4))
        plt.bar(["Edad promedio"], [avg_age], color="orange")
        plt.ylabel("Edad (años)")
        plt.title("Edad promedio de registro")
        plt.tight_layout()
        path = os.path.join(self.output_dir, "average_age.png")
        plt.savefig(path)
        plt.close()
        print(f"📈 Gráfico guardado en: {path}")

    def generate_visualizations(self, stats):
        self.plot_gender_distribution(stats.get("gender_distribution"))
        self.plot_registered_age(stats.get("average_registered_age"))
