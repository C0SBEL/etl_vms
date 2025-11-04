import statistics
import math
from collections import Counter
from datetime import datetime

class Transformer:
    def __init__(self):
        self.users = []
        self.statistics = {}

    def average_time_registered(self):
        registered_times = [
            u["registered"]["age"]
            for u in self.users
            if "registered" in u and "age" in u["registered"]
        ]

        if not registered_times:
            return None

        total = sum(registered_times)
        count = len(registered_times)
        avg = total / count
        avg_rounded = round(avg, 2)

        self.statistics["average_time_registered"] = avg_rounded
        return avg_rounded

    def gender_distribution(self):
        genders = [u["gender"] for u in self.users if "gender" in u]
        total = len(genders)
        if total == 0:
            return {}
        dist = {
            "male": round(genders.count("male") / total * 100, 2),  # Redondear
            "female": round(genders.count("female") / total * 100, 2),  # Redondear
        }
        self.statistics["gender_distribution"] = dist
        return dist

    def top_5_ancient (self, top_n: int = 5 ):
        valid_users = [user for user in self.users if 'registered' in user]
        ordered_users = sorted( valid_users, key=lambda user: user['registered']['age'],
            reverse=True)
        top_users = ordered_users[:top_n]
        formatted_top_users = []
        for user in top_users:
            formatted_top_users.append({
                'nombre_completo': f"{user['name']['first']} {user['name']['last']}",
                'email': user['email'],
                'antiguedad_años': user['registered']['age'],
                'fecha_registro': user['registered']['date']
            })
        self.statistics["top_5_ancient"] = formatted_top_users
        return formatted_top_users
        
    def total_users(self):
        total = len(self.users)
        self.statistics["total_users"] = total
        return total

    def country_distribution(self):
        countries = [u["location"]["country"] for u in self.users if "location" in u and "country" in u["location"]]
        total = len(countries)
        if total == 0:
            return {}
        country_dist = {}
        for country in countries:
            count = countries.count(country)
            country_dist[country] = round(count / total * 100, 2)

        self.statistics["country_distribution"] = country_dist
        return country_dist

    def age_registered_correlation(self):
        ages = [user["dob"]["age"] for user in self.users if
                "dob" in user and "age" in user["dob"] and "registered" in user and "age" in user["registered"]]
        registered_years = [user["registered"]["age"] for user in self.users if
                            "registered" in user and "age" in user["registered"]]

        if len(ages) < 2:
            return None

        mean_age = statistics.mean(ages)
        mean_reg = statistics.mean(registered_years)

        numerator = sum(
            (a - mean_age) * (r - mean_reg)
            for a, r in zip(ages, registered_years)
        )
        denom_x = sum((a - mean_age) ** 2 for a in ages)
        denom_y = sum((r - mean_reg) ** 2 for r in registered_years)

        if denom_x == 0 or denom_y == 0:
            return None

        correlation = numerator / math.sqrt(denom_x * denom_y)
        rounded = round(correlation, 4)
        self.statistics["age_registered_correlation"] = rounded
        return rounded

    def registration_timeline(self):
        years = []
        for user in self.users:
            if "registered" in user and "date" in user["registered"]:
                try:
                    dt = datetime.fromisoformat(user["registered"]["date"].replace('Z', '+00:00'))
                    years.append(dt.year)
                except:
                    pass

        if not years:
            return None

        year_counts = Counter(years)  # Contar registros por año
        sorted_timeline = dict(sorted(year_counts.items()))  # Ordenar por año

        timeline_stats = {
            "yearly_registrations": sorted_timeline,
            "total_years": len(sorted_timeline),
            "earliest_year": min(years),
            "latest_year": max(years),
            "peak_year": max(year_counts, key=year_counts.get),
            "peak_year_count": max(year_counts.values())
        }

        self.statistics["registration_timeline"] = timeline_stats
        return timeline_stats

    def registration_seasonality(self):
        months = []
        for user in self.users:
            if "registered" in user and "date" in user["registered"]:
                try:
                    months.append(datetime.fromisoformat(user["registered"]["date"].replace('Z', '+00:00')).month)
                except:
                    pass

        if not months:
            return None

        month_counts = Counter(months)  # Contar registros por mes
        monthly_registrations = {month: month_counts.get(month, 0) for month in
                                 range(1, 13)}  # Diccionario ordenado (1-12)

        self.statistics["registration_seasonality"] = monthly_registrations
        return monthly_registrations

    def age_distribution(self):
        age_distribution = [user["dob"]["age"] for user in self.users if "dob" in user]
        if not age_distribution:
            return None
        age_dist = {
            "average": statistics.mean(age_distribution),
            "stdev": statistics.stdev(age_distribution),
            "max": max(age_distribution),
            "min": min(age_distribution)
        }
        self.statistics["age_distribution"] = age_dist
        return age_dist

    def age_groups_distribution(self):
        ages = [user["dob"]["age"] for user in self.users if "dob" in user and "age" in user["dob"]]
        if not ages:
            return None

        groups = {"18-29": 0, "30-49": 0, "50-69": 0, "70+": 0}
        for age in ages:
            if age < 30:
                groups["18-29"] += 1
            elif age < 45:
                groups["30-49"] += 1
            elif age < 60:
                groups["50-69"] += 1
            else:
                groups["70+"] += 1

        for g in groups:
            groups[g] = round(groups[g])

        self.statistics["age_groups_distribution"] = groups
        return groups

    def latest_user(self):
        valid_users = [user for user in self.users if 'registered' in user]
        ordered_users = sorted(valid_users, key=lambda user: user['registered']['age'],
                               reverse=False)
        top_users = ordered_users[1]

        if top_users:
            name = f"{top_users['name']['first']} {top_users['name']['last']}"
            country = top_users['location']['country']
            latest_date = top_users['registered']['date']
            print("📅 Last registered user:")
            print(f"   Name: {name}")
            print(f"   Country: {country}")
            print(f"   Date: {latest_date}")

        self.statistics["latest_user"] = top_users

    def transform(self, users):
        self.users = users

        #Llamar a los métodos para calcular las estadísticas
        self.average_time_registered()
        self.gender_distribution()
        self.total_users()
        self.top_5_ancient()
        self.country_distribution()
        self.age_distribution()
        self.registration_seasonality()
        self.registration_timeline()
        self.age_registered_correlation()
        self.age_groups_distribution()
        self.latest_user()
        #Devuelve el diccionario de estadísticas
        return self.statistics
