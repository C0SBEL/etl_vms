import statistics
import math
from collections import Counter
from datetime import datetime

class Transformer:
    def __init__(self):
        self.users = []
        self.statistics = {}


    def total_users(self):
        total = len(self.users)
        self.statistics["total_users"] = total
        return total

    def years_registered_stats(self):
        registered_times = [
            u["registered"]["age"]
            for u in self.users
            if "registered" in u and "age" in u["registered"]
        ]
        if not registered_times:
            return None

        stats = {
            "average": round(statistics.mean(registered_times), 2),
            "median": round(statistics.median(registered_times), 2),
            "stdev": round(statistics.stdev(registered_times), 2) if len(registered_times) > 1 else 0,
            "min": min(registered_times),
            "max": max(registered_times)
        }

        self.statistics["years_registered_stats"] = stats
        return stats

    def age_registered_correlation(self):
        ages = [
            user["dob"]["age"] for user in self.users
            if "dob" in user and "age" in user["dob"]
            and "registered" in user and "age" in user["registered"]
        ]
        registered_years = [
            user["registered"]["age"] for user in self.users
            if "registered" in user and "age" in user["registered"]
        ]

        if len(ages) < 2:
            return None

        mean_age = statistics.mean(ages)
        mean_reg = statistics.mean(registered_years)
        numerator = sum((a - mean_age) * (r - mean_reg) for a, r in zip(ages, registered_years))
        denom_x = sum((a - mean_age) ** 2 for a in ages)
        denom_y = sum((r - mean_reg) ** 2 for r in registered_years)

        if denom_x == 0 or denom_y == 0:
            return None

        correlation = numerator / math.sqrt(denom_x * denom_y)
        rounded = round(correlation, 4)
        self.statistics["age_registered_correlation"] = rounded
        return rounded

    def gender_distribution(self):
        genders = [u["gender"] for u in self.users if "gender" in u]
        total = len(genders)
        if total == 0:
            return {}

        dist = {
            "male": round(genders.count("male") / total * 100, 2),
            "female": round(genders.count("female") / total * 100, 2),
        }
        self.statistics["gender_distribution"] = dist
        return dist

    def country_distribution(self):
        countries = [
            u["location"]["country"]
            for u in self.users
            if "location" in u and "country" in u["location"]
        ]
        total = len(countries)
        if total == 0:
            return {}

        country_dist = {}
        for country in countries:
            count = countries.count(country)
            country_dist[country] = round(count / total * 100, 2)

        self.statistics["unique_countries"] = len(set(countries))
        self.statistics["country_distribution"] = country_dist
        return country_dist

    def age_distribution(self):
        ages = [user["dob"]["age"] for user in self.users if "dob" in user]
        if not ages:
            return None

        age_dist = {
            "average": statistics.mean(ages),
            "stdev": statistics.stdev(ages),
            "max": max(ages),
            "min": min(ages)
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
            elif age < 50:
                groups["30-49"] += 1
            elif age < 70:
                groups["50-69"] += 1
            else:
                groups["70+"] += 1

        for g in groups:
            groups[g] = round(groups[g])

        self.statistics["age_groups_distribution"] = groups
        return groups

    def top_5_ancient(self, top_n: int = 5):
        valid_users = [user for user in self.users if "registered" in user]
        ordered_users = sorted(valid_users, key=lambda u: u["registered"]["age"], reverse=True)
        top_users = ordered_users[:top_n]

        formatted = [{
            "nombre_completo": f"{u['name']['first']} {u['name']['last']}",
            "email": u["email"],
            "antiguedad_años": u["registered"]["age"],
            "fecha_registro": u["registered"]["date"]
        } for u in top_users]

        self.statistics["top_5_ancient"] = formatted
        return formatted

    def registration_timeline(self):
        years = []
        for user in self.users:
            if "registered" in user and "date" in user["registered"]:
                try:
                    dt = datetime.fromisoformat(user["registered"]["date"].replace("Z", "+00:00"))
                    years.append(dt.year)
                except:
                    pass

        if not years:
            return None

        year_counts = Counter(years)
        sorted_timeline = dict(sorted(year_counts.items()))

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
        genders = []

        for user in self.users:
            if "registered" in user and "date" in user["registered"] and "gender" in user:
                try:
                    month = datetime.fromisoformat(user["registered"]["date"].replace('Z', '+00:00')).month
                    months.append(month)
                    genders.append(user["gender"])
                except:
                    pass

        if not months:
            return None

        # Contar registros totales por mes
        month_counts = Counter(months)
        monthly_registrations = {month: month_counts.get(month, 0) for month in range(1, 13)}

        # Contar registros por mes y género
        monthly_by_gender = {
            "male": {month: 0 for month in range(1, 13)},
            "female": {month: 0 for month in range(1, 13)}
        }

        for month, gender in zip(months, genders):
            if gender in ["male", "female"]:
                monthly_by_gender[gender][month] += 1

        self.statistics["registration_seasonality"] = {
            "total": monthly_registrations,
            "by_gender": monthly_by_gender
        }

        return self.statistics["registration_seasonality"]

    def latest_user(self):
        valid_users = [u for u in self.users if "registered" in u and "date" in u["registered"]]
        if not valid_users:
            return None

        latest_user = max(valid_users, key=lambda u: u["registered"]["date"])

        self.statistics["latest_user"] = latest_user
        return latest_user

    def user_retention_analysis(self):
        """Analiza qué usuarios podrían considerarse 'activos' basado en antigüedad"""
        if not self.users:
            return None

        registered_ages = [user["registered"]["age"] for user in self.users
                           if "registered" in user and "age" in user["registered"]]

        if not registered_ages:
            return None

        # Categorizar usuarios
        new_users = [age for age in registered_ages if age < 2]
        established = [age for age in registered_ages if 2 <= age < 5]
        veterans = [age for age in registered_ages if 5 <= age < 10]
        legends = [age for age in registered_ages if age >= 10]

        total = len(registered_ages)

        retention = {
            "new_users_0-2y": {
                "count": len(new_users),
                "percentage": round(len(new_users) / total * 100, 2)
            },
            "established_2-5y": {
                "count": len(established),
                "percentage": round(len(established) / total * 100, 2)
            },
            "veterans_5-10y": {
                "count": len(veterans),
                "percentage": round(len(veterans) / total * 100, 2)
            },
            "legends_10y+": {
                "count": len(legends),
                "percentage": round(len(legends) / total * 100, 2)
            }
        }

        self.statistics["user_retention_analysis"] = retention
        return retention

    def most_common_names(self, top_n=10):
        """Nombres y apellidos más comunes"""
        first_names = [user["name"]["first"].title() for user in self.users
                       if "name" in user and "first" in user["name"]]
        last_names = [user["name"]["last"].title() for user in self.users
                      if "name" in user and "last" in user["name"]]

        if not first_names or not last_names:
            return None

        names_stats = {
            "top_first_names": dict(Counter(first_names).most_common(top_n)),
            "top_last_names": dict(Counter(last_names).most_common(top_n)),
            "unique_first_names": len(set(first_names)),
            "unique_last_names": len(set(last_names))
        }

        self.statistics["most_common_names"] = names_stats
        return names_stats

    def transform(self, users):
        self.users = users

        self.total_users()
        self.years_registered_stats()
        self.gender_distribution()
        self.country_distribution()
        self.age_distribution()
        self.age_groups_distribution()
        self.top_5_ancient()
        self.registration_timeline()
        self.registration_seasonality()
        self.age_registered_correlation()
        self.latest_user()
        self.most_common_names()
        self.user_retention_analysis()

        return self.statistics
