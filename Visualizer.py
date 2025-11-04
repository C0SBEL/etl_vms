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
        """Gráfico de barras de registros por mes"""
        monthly_reg = self.stats.get("registration_seasonality")
        if not monthly_reg:
            return
        
        # Datos básicos
        MONTH_NAMES = ["Ene", "Feb", "Mar", "Abr", "May", "Jun", "Jul", "Ago", "Sep", "Oct", "Nov", "Dic"]
        months = list(monthly_reg.keys())
        counts = list(monthly_reg.values())
        
        # Crear el gráfico
        plt.figure(figsize=(10, 6))
        plt.bar(months, counts, color='skyblue', edgecolor='black')
        
        # Etiquetas en las barras
        for month, count in zip(months, counts):
            plt.text(month, count, str(count), ha='center', va='bottom', fontweight='bold')
        
        # Configuración
        plt.xlabel('Mes')
        plt.ylabel('Registros')
        plt.title(f'Registros por Mes - Total: {sum(counts):,} usuarios')
        plt.xticks(months, MONTH_NAMES, rotation=45)
        plt.grid(True, alpha=0.3, axis='y')
        plt.tight_layout()
        
        # Guardar
        path = os.path.join(self.output_dir, "registration_seasonality.png")
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
