import random


class Cube:
    def __init__(self):
        self.opened = False


class FemaleStudent:
    def __init__(
        self,
        base_calorie_requirement,
        daily_water_requirement,
        survival_ability,
        sickness_probability,
        injury_probability,
    ):
        self.food = 0
        self.water = 0
        self.base_calorie_requirement = base_calorie_requirement
        self.daily_water_requirement = daily_water_requirement
        self.survival_ability = survival_ability
        self.sickness_probability = sickness_probability
        self.injury_probability = injury_probability
        self.current_health = 100
        self.injury = 0
        self.stress = 0

    def consume_food(self, amount):
        self.food -= amount

    def consume_water(self, amount):
        self.water -= amount


class Simulation:
    def __init__(self, num_cubes):
        self.cubes = [Cube() for _ in range(num_cubes)]
        self.students = [
            FemaleStudent(
                base_calorie_requirement=random.randint(1800, 2200),
                daily_water_requirement=random.randint(2000, 3000),
                survival_ability=random.random(),
                sickness_probability=random.uniform(0.01, 0.1),
                injury_probability=random.uniform(0.01, 0.1),
            )
            for _ in range(num_cubes)
        ]
        self.opened_cubes = 0
        self.dead_students = 0
        self.days_survived = 0

    def reset(self):
        for student in self.students:
            student.food = 0
            student.water = 0
            student.current_health = 100
            student.injury = 0
            student.stress = 0
        for cube in self.cubes:
            cube.opened = False
            self.opened_cubes = 0
            self.dead_students = 0
            self.days_survived = 0

    def open_door(self, cube_index):
        if not self.cubes[cube_index].opened:
            self.cubes[cube_index].opened = True
            self.opened_cubes += 1

    def run(self):
        self.reset()

        cube_indices = random.sample(range(len(self.cubes)), len(self.students))

        for index in cube_indices:
            self.open_door(index)

        while len(self.students) > 1:
            for i, student in enumerate(self.students):
                calorie_requirement = student.base_calorie_requirement
                water_requirement = student.daily_water_requirement

            # 病気になる確率に基づいて、健康状態を減らします。
            if random.random() < student.sickness_probability:
                student.current_health -= random.randint(1, 20)

            # 負傷する確率に基づいて、負傷レベルを増加させます。
            if random.random() < student.injury_probability:
                student.injury += random.randint(1, 20)
            # ストレスを増やします。
            student.stress += random.uniform(0.1, 1)

            # 食べ物と水を消費します。
            student.consume_food(calorie_requirement)
            student.consume_water(water_requirement)

            # 健康状態が100より低い場合、基本的なカロリー要件を追加します。
            if student.current_health < 100:
                student.base_calorie_requirement += 100

            # 生存者が死亡する場合、リストから削除します。
            if student.food <= 0 or student.water <= 0 or student.stress >= 100:
                self.students.pop(i)
                self.dead_students += 1
                for j in range(min(50, len(self.students))):
                    self.students[j].food += (
                        1 + self.students[j].survival_ability
                    ) * 2000
                    self.students[j].water += (
                        1 + self.students[j].survival_ability
                    ) * 2500

            self.days_survived += 1
        return self.opened_cubes, self.dead_students, self.days_survived


def days_to_years_and_days(days):
    years = days // 365  # 整数の年数を計算します。
    leap_years = years // 4  # うるう年の数を計算します。
    days -= years * 365 + leap_years  # 残りの日数を計算します。
    return years, days


print("Enter the number of cubes:")
num_cubes = int(input())
simulation = Simulation(num_cubes)
opened_cubes, dead_students, days_survived = simulation.run()

print(f"Opened cubes: {opened_cubes}")
print(f"Dead students: {dead_students}")
print(f"Days survived: {days_survived}")
years, days = days_to_years_and_days(days_survived)
print(f"{years}年{days}日生き残りました。")
