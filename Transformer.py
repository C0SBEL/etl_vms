import statistics
from itertools import count


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

    def ask_name(self):
        try:
            name = input("Whats' your name?").strip()
        except EOFError:
            name = ""
        target = name.lower()
        count = 0

        for u in self.users:
            try:
                if u["name"]["first"] == target:
                    count += 1
            except Exception:
                continue

            self.statistics["ask_name"] = count

        return count



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
        self.age_distribution()
        self.age_groups_distribution()
        self.latest_user()
        self.ask_name()

        #Devuelve el diccionario de estadísticas
        return self.statistics
