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

    def total_users(self):
        total = len(self.users)
        self.statistics["total_users"] = total
        return total

    def transform(self, users):
        self.users = users

        #Llamar a los métodos para calcular las estadísticas
        self.average_time_registered()
        self.gender_distribution()
        self.total_users()

        #Devuelve el diccionario de estadísticas
        return self.statistics
