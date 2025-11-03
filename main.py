from etl.controller.ETLController import ETLController
from etl.services.Extractor import Extractor
from etl.services.Transformer import Transformer
from etl.services.Visualizer import Visualizer
from etl.services.Loader import Loader
from config.settings import BASE_DIR
import os


def main():
    print("🚀 Iniciando ejecución principal...")

    # Configurar rutas de salida basadas en BASE_DIR
    vis_path = os.path.join(BASE_DIR, "data", "output", "visualizations")
    db_path = os.path.join(BASE_DIR, "data", "database", "etl_results.db")

    # Instanciar servicios
    extractor = Extractor(base_url="https://randomuser.me/api/", num_users=5000)
    transformer = Transformer()
    visualizer = Visualizer(output_dir=vis_path, clean=True)
    loader = Loader(db_path=db_path, reset=True)

    # Ejecutar ETL
    controller = ETLController(extractor, transformer, visualizer, loader)
    controller.run()


if __name__ == "__main__":
    main()
