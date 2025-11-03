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

    def transform(self, users):
        self.users = users

        #Llamar a los métodos para calcular las estadísticas
        self.average_time_registered()
        self.gender_distribution()
        self.total_users()
        self.top_5_ancient()
        self.country_distribution()

        #Devuelve el diccionario de estadísticas
        return self.statistics
