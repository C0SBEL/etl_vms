from userExtractor import UserExtractor
from userTransformer import UserTransformer


class ETLController:
    def __init__(self, extractor, transformer):
        self.extractor = extractor
        self.transformer = transformer

    def run(self):
        data = self.extractor.get_users()
        self.transformer.data = data.get("results", [])
        return self.transformer.transform()

if __name__ == "__main__":
    extractor = UserExtractor("https://randomuser.me/api/", num_users=5000)
    transformer = UserTransformer({})
    controller = ETLController(extractor, transformer)

    results = controller.run()

    print("\n=== Estadísticas de los usuarios extraídos ===")
    print(f"Usuarios totales: {results['total_users']}")
    print(f"Edad media desde el registro: {results['average_registered_age']:.2f} años")
    print("Distribución por género:")
    print(f"  Hombres: {results['gender_distribution']['male']:.2f}%")
    print(f"  Mujeres: {results['gender_distribution']['female']:.2f}%")
