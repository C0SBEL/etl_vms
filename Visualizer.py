import os
import matplotlib.pyplot as plt

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
            return

        gender_dist = self.stats.get("gender_distribution")
        if not gender_dist:
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
            return

        avg_time = self.stats.get("average_time_registered")
        #if avg_time is None:
        #    print("⚠️ No hay estadística de tiempo registrado promedio.")

        plt.figure(figsize=(8, 5))
        plt.hist(times, bins=10, color="skyblue", edgecolor="black")
        plt.xlabel("Años registrados")
        plt.ylabel("Número de usuarios")
        plt.title("Distribución del tiempo que los usuarios llevan registrados")

        # Línea de referencia de la media
        plt.axvline(avg_time, color="red", linestyle="dashed", linewidth=2)
        plt.text(avg_time + 0.1, plt.ylim()[1] * 0.9, f"Media = {avg_time} años", color="red")

        path = os.path.join(self.output_dir, "registered_time_distribution.png")
        plt.tight_layout()
        plt.savefig(path)
        plt.close()
    
    def plot_age_registered_correlation(self):
        """Visualiza la correlación entre edad de usuarios y años registrados."""
        ages = []
        registered_years = []
        
        for user in self.users:
            age = user.get("dob", {}).get("age")
            reg_age = user.get("registered", {}).get("age")
            if age is not None and reg_age is not None:
                ages.append(age)
                registered_years.append(reg_age)
        
        if len(ages) < 2:
            return
        
        correlation = self.stats.get("age_registered_correlation")
        if correlation is None:
            return
             
        # Calcular línea de tendencia
        n = len(ages)
        sum_x = sum(ages)
        sum_y = sum(registered_years)
        sum_xy = sum(x * y for x, y in zip(ages, registered_years))
        sum_x2 = sum(x ** 2 for x in ages)
        m = (n * sum_xy - sum_x * sum_y) / (n * sum_x2 - sum_x ** 2)
        b = (sum_y - m * sum_x) / n
        
        sorted_ages = sorted(ages)
        trend_line = [m * x + b for x in sorted_ages]
        
        plt.figure(figsize=(10, 6))
        plt.scatter(ages, registered_years, alpha=0.5, color="steelblue", edgecolors="black", linewidth=0.5)
        plt.plot(sorted_ages, trend_line, "r--", linewidth=2, label="Línea de tendencia")
        plt.xlabel("Edad del usuario (años)")
        plt.ylabel("Años registrado en el sistema")
        plt.title(f"Correlación entre Edad y Antigüedad\n(Coeficiente: {correlation})")
        plt.legend()
        plt.grid(True, alpha=0.3)
        plt.tight_layout()
        
        path = os.path.join(self.output_dir, "age_registered_correlation.png")
        plt.savefig(path)
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
        m = sum((x - mx) * (y - my) for x, y in zip(years, counts)) / sum((x - mx)**2 for x in years)
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
                plt.text(month, male/2, str(male), ha='center', va='center', 
                        fontsize=8, color='white', fontweight='bold')
            # Mujeres en el medio de su sección
            if female > 15:  # Solo si hay espacio suficiente
                plt.text(month, male + female/2, str(female), ha='center', va='center', 
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
        #legend.get_frame().set_facecolor('white')
        legend.get_frame().set_edgecolor('#E0E0E0')
        
        # Título más elegante
        plt.title('Distribución por antigüedad de usuarios', 
                fontsize=18, fontweight='bold', color='#2C3E50', pad=20)
        
        # Subtítulo con contexto adicional
        #plt.text(0.5, 1.05, 'Distribución por antigüedad en el sistema', ha='center', va='top', transform=ax.transAxes, fontsize=12, color='#7F8C8D', style='italic')
        
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
            ax1.text(width, bar.get_y() + bar.get_height()/2, 
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
            ax2.text(width, bar.get_y() + bar.get_height()/2, 
                    f' {count}', ha='left', va='center', fontweight='bold', fontsize=10)
        
        plt.tight_layout()
        
        # Guardar
        path = os.path.join(self.output_dir, "most_common_names.png")
        plt.savefig(path, dpi=300, bbox_inches='tight')
        plt.close()
 
    def generate_visualizations(self, users, stats):
        if users:
            self.users = users
        else:
            return

        self.stats = stats

        #Métodos de visualización
        self.plot_gender_distribution()
        self.plot_time_registered_distribution()
        self.plot_age_registered_correlation()
        self.plot_registration_timeline()
        self.plot_registration_seasonality()
        self.plot_user_retention_analysis() 
        self.plot_most_common_names()
