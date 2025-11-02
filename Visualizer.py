import os
import matplotlib.pyplot as plt

class Visualizer:
    def __init__(self, output_dir="results"):
        self.output_dir = output_dir
        os.makedirs(self.output_dir, exist_ok=True)

    def plot_gender_distribution(self, gender_distribution):
        if not gender_distribution:
            print("No hay datos de género para graficar.")
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
        plt.figure(figsize=(4, 4))
        plt.bar(["Edad promedio"], [avg_age], color="orange")
        plt.ylabel("Edad (años)")
        plt.title("Edad promedio de registro")
        plt.tight_layout()
        path = os.path.join(self.output_dir, "average_age.png")
        plt.savefig(path)
        plt.close()
        print(f"📈 Gráfico guardado en: {path}")
