# ETL_VMS

ETL_VMS es un proyecto de **ETL (Extract, Transform, Load)** que permite extraer datos de usuarios, transformarlos para calcular estadísticas y generar visualizaciones, y finalmente almacenar tanto los datos como los resultados en una base de datos SQLite y archivos gráficos.  

---

## Estructura del proyecto

```
etl_vms/
├── config/
│   ├── __init__.py
│   └── settings.py
├── data/
│   ├── output/
│   │   └── visualizations/   # Gráficos generados
│   └── database/
│       └── etl_results.db    # Base de datos SQLite
├── etl/
│   ├── controller/
│   │   ├── ETLController.py  # Controla el flujo ETL
│   ├── services/
│   │   ├── Extractor.py      # Extracción de datos
│   │   ├── Transformer.py    # Transformación y estadísticas
│   │   ├── Loader.py         # Persistencia de datos y estadísticas
│   │   └── Visualizer.py     # Generación de gráficos
├── main.py                   # Script principal
├── README.md
└── requirements.txt
```

---

## Instalación

1. Clonar el repositorio:

```bash
git clone https://gitlab.com/agusticostabellamoreno/etl_vms.git
cd etl_vms
```

2. Crear y activar un entorno virtual:

```bash
python3 -m venv .venv
source .venv/bin/activate  # En Windows: .venv\Scripts\activate
```

3. Instalar dependencias:

```bash
pip install -r requirements.txt
```

---

## Uso

Ejecutar el flujo completo ETL desde el script principal:

```bash
python main.py
```

Esto realizará:

1. **Extracción de usuarios** mediante `Extractor.py`.
2. **Transformación** de los datos y cálculo de estadísticas con `Transformer.py`.
3. **Persistencia** en la base de datos SQLite mediante `Loader.py`.
4. **Generación de visualizaciones** en `data/output/visualizations` mediante `Visualizer.py`.

---

## Almacenamiento de datos

- **Base de datos:** `data/database/etl_results.db` contiene los usuarios extraídos y las estadísticas calculadas.  
- **Visualizaciones:** `data/output/visualizations` contiene gráficos generados automáticamente.

---

## Autores

- **Ferran Tubert**
- **Paulina Peralta**
- **Blanca Gallardo**
- **Agustí Costabella** 


