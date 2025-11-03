from Extractor import Extractor
from Transformer import Transformer


class ETLController:
    def __init__(self, extractor, transformer):
        self.extractor = extractor
        self.transformer = transformer

    def run(self):
        data = self.extractor.get_users()
        self.transformer.data = data.get("results", [])
        return self.transformer.transform()

if __name__ == "__main__":
    extractor = Extractor("https://randomuser.me/api/", num_users=5000)
    transformer = Transformer({})
    controller = ETLController(extractor, transformer)

    results = controller.run()

    print("\n=== Estadísticas de los usuarios extraídos ===")
    print(f"Usuarios totales: {results['total_users']}")
    print(f"Edad media desde el registro: {results['average_registered_age']:.2f} años")
    print("Distribución por género:")
    print(f"  Hombres: {results['gender_distribution']['male']:.2f}%")
    print(f"  Mujeres: {results['gender_distribution']['female']:.2f}%")
    print("Top 5 usuarios con más antigüedad:")
    if results['top_5_ancient']:
        for i, user in enumerate(results['top_5_ancient']):
            print(f"  {i + 1}. {user['nombre_completo']}")
            print(f"     -> Antigüedad: {user['antiguedad_años']} años (Registro: {user['fecha_registro']})")
    else:
        print("No se encontraron suficientes usuarios para el Top 5.")