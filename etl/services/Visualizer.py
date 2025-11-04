import os
import statistics
import seaborn as sns
import matplotlib.pyplot as plt
import geopandas as gpd
import simplekml

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

        stats = self.stats.get("years_registered_stats")
        if not stats:
            print("⚠️ No hay estadísticas de tiempo registrado.")
            return

        # Crear bins alineados con años enteros
        min_year, max_year = int(min(times)), int(max(times))
        bins = range(min_year, max_year + 2)  # +2 para incluir el último borde

        plt.figure(figsize=(8, 5))
        plt.hist(times, bins=bins, color="skyblue", edgecolor="black", align="left", rwidth=0.9)
        plt.xlabel("Años registrados")
        plt.ylabel("Número de usuarios")
        plt.title("Distribución del tiempo que los usuarios llevan registrados")

        # Líneas de media y mediana
        plt.axvline(stats["average"], color="red", linestyle="dashed", linewidth=2,
                    label=f"Media = {stats['average']:.1f}")
        plt.axvline(stats["median"], color="green", linestyle="dashed", linewidth=2,
                    label=f"Mediana = {stats['median']:.1f}")

        # Ticks enteros y bien alineados
        plt.xticks(range(min_year, max_year + 1))

        plt.legend()
        plt.tight_layout()

        path = os.path.join(self.output_dir, "registered_time_distribution.png")
        plt.savefig(path, dpi=300)
        plt.close()

    def plot_registration_timeline(self):
        """Gráfico de línea mostrando la tendencia de registros por año"""
        timeline_data = self.stats.get("registration_timeline")
        if not timeline_data or "yearly_registrations" not in timeline_data:
            return

        yearly_registrations = timeline_data["yearly_registrations"]
        if not yearly_registrations:
            return

        years = list(yearly_registrations.keys())
        counts = list(yearly_registrations.values())

        # Crear el gráfico
        plt.figure(figsize=(12, 6))
        plt.plot(years, counts, marker='o', linewidth=2, markersize=8, color='steelblue')

        # Calcular y dibujar línea de tendencia
        n = len(years)
        mx, my = sum(years) / n, sum(counts) / n
        m = sum((x - mx) * (y - my) for x, y in zip(years, counts)) / sum((x - mx) ** 2 for x in years)
        b = my - m * mx

        trend_line = [m * x + b for x in years]
        plt.plot(years, trend_line, "r--", linewidth=2,
                 label=f'Tendencia: {"↗ Crecimiento" if m > 0 else "↘ Decrecimiento"}')

        # Configuración
        plt.xlabel("Año de Registro")
        plt.ylabel("Usuarios Registrados")
        plt.title(f"Registros por Año ({timeline_data['earliest_year']}-{timeline_data['latest_year']})")
        plt.grid(True, alpha=0.3)
        plt.legend()

        if len(years) > 10:
            plt.xticks(rotation=45)

        plt.tight_layout()

        plt.savefig(os.path.join(self.output_dir, "registration_timeline.png"), dpi=300)
        plt.close()

    def plot_registration_seasonality(self):
        """Gráfico de barras apiladas de registros por mes separado por género"""
        monthly_data = self.stats.get("registration_seasonality")
        if not monthly_data:
            return

        # Datos básicos
        MONTH_NAMES = ["Ene", "Feb", "Mar", "Abr", "May", "Jun", "Jul", "Ago", "Sep", "Oct", "Nov", "Dic"]
        months = list(range(1, 13))

        # Extraer datos por género
        male_counts = [monthly_data["by_gender"]["male"][m] for m in months]
        female_counts = [monthly_data["by_gender"]["female"][m] for m in months]
        total_counts = [monthly_data["total"][m] for m in months]

        # Crear el gráfico con barras apiladas
        plt.figure(figsize=(12, 6))

        # Primera barra (varones en la base)
        bars1 = plt.bar(months, male_counts, label='Varones',
                        color='steelblue', edgecolor='black')

        # Segunda barra (mujeres encima de varones)
        bars2 = plt.bar(months, female_counts, bottom=male_counts, label='Mujeres',
                        color='darksalmon', edgecolor='black')

        # Etiquetas en las barras - mostrar totales arriba
        for i, (month, total, male, female) in enumerate(zip(months, total_counts, male_counts, female_counts)):
            # Total arriba de todo
            plt.text(month, total, str(total), ha='center', va='bottom',
                     fontsize=9, fontweight='bold')
            # Varones en el medio de su sección
            if male > 15:  # Solo si hay espacio suficiente
                plt.text(month, male / 2, str(male), ha='center', va='center',
                         fontsize=8, color='white', fontweight='bold')
            # Mujeres en el medio de su sección
            if female > 15:  # Solo si hay espacio suficiente
                plt.text(month, male + female / 2, str(female), ha='center', va='center',
                         fontsize=8, color='white', fontweight='bold')

        # Configuración
        plt.xlabel('Mes', fontsize=12)
        plt.ylabel('Registros', fontsize=12)
        total = sum(total_counts)
        plt.title(f'Registros por Mes según Género - Total: {total:,} usuarios',
                  fontsize=14, fontweight='bold')
        plt.xticks(months, MONTH_NAMES, rotation=45)
        plt.legend(loc='upper right', fontsize=10)
        plt.grid(True, alpha=0.3, axis='y')
        plt.tight_layout()

        # Guardar
        path = os.path.join(self.output_dir, "registration_seasonality.png")
        plt.savefig(path, dpi=300, bbox_inches='tight')
        plt.close()

    def plot_age_vs_registered_heatmap(self):
        """Heatmap de franjas de edad (24–42, 43–61, 62–80) vs años registrados (3–9, 10–16, 17–23)."""

        # Verificar que haya datos
        if not self.users:
            print("⚠️ No hay usuarios para generar el heatmap.")
            return

        # Definir franjas fijas
        age_bins = [24, 43, 62, 81]  # 24–42, 43–61, 62–80
        reg_bins = [3, 10, 17, 24]  # 3–9, 10–16, 17–23

        # Inicializar matriz 3x3
        heatmap_data = [[0 for _ in range(3)] for _ in range(3)]

        # Llenar matriz
        for u in self.users:
            age = u.get("dob", {}).get("age")
            reg = u.get("registered", {}).get("age")
            if age is None or reg is None:
                continue

            # Encontrar índice de grupo de edad
            age_idx = next((i for i in range(3) if age_bins[i] <= age < age_bins[i + 1]), None)
            # Encontrar índice de grupo de años registrados
            reg_idx = next((i for i in range(3) if reg_bins[i] <= reg < reg_bins[i + 1]), None)

            if age_idx is not None and reg_idx is not None:
                heatmap_data[age_idx][reg_idx] += 1

        # Graficar heatmap
        plt.figure(figsize=(8, 6))
        sns.heatmap(
            heatmap_data,
            annot=True,
            fmt="d",
            cmap="YlGnBu",
            xticklabels=["3–9", "10–16", "17–23"],
            yticklabels=["24–42", "43–61", "62–80"]
        )
        plt.xlabel("Años registrados")
        plt.ylabel("Edad del usuario")
        plt.title("Heatmap: usuarios por franjas de edad vs años registrados")
        plt.tight_layout()

        path = os.path.join(self.output_dir, "age_vs_registered_heatmap.png")
        plt.savefig(path, dpi=300)
        plt.close()

    def plot_country_choropleth(self):
        country_dist = self.stats.get("country_distribution")
        if not country_dist:
            print("⚠️ No hay datos de países para generar el cartograma.")
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

    def plot_avg_by_country(self, top_n: int = 10):
        valid_users = [
            u for u in self.users
            if "location" in u and "country" in u["location"] and "dob" in u and "age" in u["dob"]
        ]

        country_ages = {}
        for u in valid_users:
            country = u["location"]["country"]
            age = u["dob"]["age"]
            try:
                age_val = float(age)
            except (TypeError, ValueError):
                continue
            country_ages.setdefault(country, []).append(age_val)

        avg_by_country = {
            country: round(statistics.mean(ages), 1)
            for country, ages in country_ages.items() if ages
        }

        ordered_countries = sorted(
            avg_by_country.items(),
            key=lambda item: item[1],
            reverse=True
        )
        top_countries = ordered_countries[:top_n]

        # Fix: comprovar llista real obtinguda
        if not top_countries:
            print("⚠️ No data.")
            return

        countries = [c for c, _ in top_countries]
        values = [v for _, v in top_countries]

        plt.figure(figsize=(10, 6))
        bars = plt.bar(countries, values, color="steelblue")

        plt.title(f"Age average (Top {top_n})")
        plt.ylabel("Age average")
        plt.xlabel("Country")
        plt.xticks(rotation=45, ha="right")

        for bar, val in zip(bars, values):
            plt.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 0.3, f"{val}", ha="center", va="bottom")

        plt.tight_layout()
        path = os.path.join(self.output_dir, "avg_age_by_country.png")
        plt.savefig(path)
        plt.close()

    def plot_user_retention_analysis(self):
        """Gráfico de dona mostrando la distribución de usuarios por antigüedad"""
        retention_data = self.stats.get("user_retention_analysis")
        if not retention_data:
            return

        # Preparar datos
        categories = ["Nuevos\n(0-2 años)", "Establecidos\n(2-5 años)",
                      "Veteranos\n(5-10 años)", "Leyendas\n(10+ años)"]
        keys = ["new_users_0-2y", "established_2-5y", "veterans_5-10y", "legends_10y+"]

        counts = [retention_data[key]["count"] for key in keys]
        percentages = [retention_data[key]["percentage"] for key in keys]

        # Paleta de colores moderna y vibrante
        colors = ['#FF6B6B', '#4ECDC4', '#45B7D1', '#FFA07A']

        # Crear figura con fondo blanco
        fig, ax = plt.subplots(figsize=(12, 8), facecolor='white')
        ax.set_facecolor('white')

        # Crear el gráfico de dona (donut chart)
        wedges, texts, autotexts = ax.pie(
            counts,
            labels=categories,
            autopct='%1.1f%%',
            colors=colors,
            startangle=90,
            # explode=(0.02, 0.02, 0.02, 0.08),  ← ELIMINAR O COMENTAR esta línea
            shadow=False,
            wedgeprops={'edgecolor': 'white', 'linewidth': 0, 'antialiased': True},
            pctdistance=0.85,
            textprops={'fontsize': 12, 'weight': 'bold'}
        )

        # Crear el círculo central para efecto dona
        centre_circle = plt.Circle((0, 0), 0.70, fc='white', linewidth=0)
        ax.add_artist(centre_circle)

        # Mejorar apariencia del texto en las porciones
        for text in texts:
            text.set_fontsize(11)
            text.set_fontweight('bold')
            text.set_color('#2C3E50')

        for autotext in autotexts:
            autotext.set_color('white')
            autotext.set_fontsize(11)
            autotext.set_fontweight('bold')

        # Texto central con información clave
        total = sum(counts)
        ax.text(0, 0.1, f'{total:,}', ha='center', va='center',
                fontsize=36, fontweight='bold', color='#2C3E50')
        ax.text(0, -0.15, 'Usuarios', ha='center', va='center',
                fontsize=16, color='#7F8C8D')

        # Crear leyenda más elegante
        legend_labels = [
            f'{cat.replace(chr(10), " ")}: {count:,} ({pct}%)'
            for cat, count, pct in zip(categories, counts, percentages)
        ]
        legend = ax.legend(
            legend_labels,
            loc='center left',
            bbox_to_anchor=(1, 0, 0.5, 1),
            fontsize=11,
            frameon=True,
            fancybox=True,
            shadow=True,
            title='Categorías',
            title_fontsize=13
        )
        # legend.get_frame().set_facecolor('white')
        legend.get_frame().set_edgecolor('#E0E0E0')

        # Título más elegante
        plt.title('Distribución por antigüedad de usuarios',
                  fontsize=18, fontweight='bold', color='#2C3E50', pad=20)

        # Subtítulo con contexto adicional
        # plt.text(0.5, 1.05, 'Distribución por antigüedad en el sistema', ha='center', va='top', transform=ax.transAxes, fontsize=12, color='#7F8C8D', style='italic')

        plt.tight_layout()

        # Guardar con alta calidad
        path = os.path.join(self.output_dir, "user_retention_analysis.png")
        plt.savefig(path, dpi=300, bbox_inches='tight', facecolor='white')
        plt.close()

    def plot_most_common_names(self):
        """Gráfico de barras horizontales dobles mostrando nombres y apellidos más comunes"""
        names_data = self.stats.get("most_common_names")
        if not names_data:
            return

        first_names = names_data.get("top_first_names", {})
        last_names = names_data.get("top_last_names", {})

        if not first_names or not last_names:
            return

        # Crear figura con dos subplots
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 8))
        fig.suptitle('Nombres y Apellidos Más Comunes', fontsize=18, fontweight='bold', y=0.98)

        # Subplot 1: Nombres más comunes
        first_names_list = list(first_names.keys())
        first_counts = list(first_names.values())

        bars1 = ax1.barh(first_names_list, first_counts, color='steelblue', edgecolor='black')
        ax1.set_xlabel('Frecuencia', fontsize=12, fontweight='bold')
        ax1.set_title(f'Top {len(first_names_list)} Nombres\n({names_data["unique_first_names"]} nombres únicos)',
                      fontsize=14, fontweight='bold', pad=10)
        ax1.invert_yaxis()  # Para que el más común esté arriba
        ax1.grid(True, alpha=0.3, axis='x')

        # Añadir valores en las barras
        for bar, count in zip(bars1, first_counts):
            width = bar.get_width()
            ax1.text(width, bar.get_y() + bar.get_height() / 2,
                     f' {count}', ha='left', va='center', fontweight='bold', fontsize=10)

        # Subplot 2: Apellidos más comunes
        last_names_list = list(last_names.keys())
        last_counts = list(last_names.values())

        bars2 = ax2.barh(last_names_list, last_counts, color='darksalmon', edgecolor='black')
        ax2.set_xlabel('Frecuencia', fontsize=12, fontweight='bold')
        ax2.set_title(f'Top {len(last_names_list)} Apellidos\n({names_data["unique_last_names"]} apellidos únicos)',
                      fontsize=14, fontweight='bold', pad=10)
        ax2.invert_yaxis()
        ax2.grid(True, alpha=0.3, axis='x')

        # Añadir valores en las barras
        for bar, count in zip(bars2, last_counts):
            width = bar.get_width()
            ax2.text(width, bar.get_y() + bar.get_height() / 2,
                     f' {count}', ha='left', va='center', fontweight='bold', fontsize=10)

        plt.tight_layout()

        # Guardar
        path = os.path.join(self.output_dir, "most_common_names.png")
        plt.savefig(path, dpi=300, bbox_inches='tight')
        plt.close()

    def kml_user_locations(self):
        """Genera un archivo KML con las ubicaciones de usuarios y devuelve un enlace local para abrirlo."""
        kml = simplekml.Kml()

        for u in self.users:
            try:
                location = u["location"]
                coords = location["coordinates"]
                lat = float(coords["latitude"])
                lon = float(coords["longitude"])

                name = f"{u['name']['first']} {u['name']['last']}"
                kml.newpoint(name=name, coords=[(lon, lat)])
            except (KeyError, ValueError):
                continue

        path = os.path.join(self.output_dir, "user_locations.kml")
        kml.save(path)

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
        self.plot_country_choropleth()
        self.plot_registration_timeline()
        self.plot_registration_seasonality()
        self.plot_age_vs_registered_heatmap()
        self.plot_avg_by_country()
        self.plot_user_retention_analysis()
        self.plot_most_common_names()
        self.kml_user_locations()
