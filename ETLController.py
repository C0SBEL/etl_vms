from Extractor import Extractor
from Transformer import Transformer
from Visualizer import Visualizer
from Loader import Loader


class ETLController:
    def __init__(self, extractor, transformer, visualizer, loader):
        self.extractor = extractor
        self.transformer = transformer
        self.visualizer = visualizer
        self.loader = loader

    def run(self):
        print("🚀 Iniciando proceso ETL...")
        print("🔍 Extrayendo datos de usuarios...")

        users = self.extractor.get_users()
        if not users:
            print("⚠️ No se extrajeron usuarios. Abortando carga y visualización.")
            return {}

        stats = self.transformer.transform(users)

        print("📊 Estadísticas generadas:")
        for key, value in stats.items():
            print(f" - {key}: {value}")

        print("📈 Generando visualizaciones...")
        self.visualizer.generate_visualizations(users, stats)

        print("💾 Cargando datos en la base de datos SQL...")
        self.loader.save_users(users)
        self.loader.save_statistics(stats)

        print("✅ Proceso ETL completado.")
        return stats


if __name__ == "__main__":
    extractor = Extractor(base_url="https://randomuser.me/api/", num_users=5000)
    transformer = Transformer()
    visualizer = Visualizer("visualizations", clean=True)
    loader = Loader(db_path="etl_results.db", reset=True)

    controller = ETLController(extractor, transformer, visualizer, loader)
    controller.run()
