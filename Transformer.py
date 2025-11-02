import statistics

class Transformer:
    def __init__(self):
        self.users = []
        self.statistics = {}

    def average_registered_age(self):
        registered_ages = [
            u["registered"]["age"]
            for u in self.users
            if "registered" in u and "age" in u["registered"]
        ]
        if not registered_ages:
            return None
        avg = statistics.mean(registered_ages)
        self.statistics["average_registered_age"] = avg
        return avg

    def gender_distribution(self):
        genders = [u["gender"] for u in self.users if "gender" in u]
        total = len(genders)
        if total == 0:
            return {}
        dist = {
            "male": genders.count("male") / total * 100,
            "female": genders.count("female") / total * 100,
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
        self.average_registered_age()
        self.gender_distribution()
        self.total_users()

        return self.statistics
