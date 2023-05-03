from model.cube import Cube
from model.female_studente import FemaleStudent
import random


class SimulationModel:
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

    def add_food(self, student, amount):
        student.food += amount
        if student.food > student.max_food:
            student.food = student.max_food

    def add_water(self, student, amount):
        student.water += amount
        if student.water > student.max_water:
            student.water = student.max_water

    def consume_food(self, student, amount):
        student.food -= amount

    def consume_water(self, student, amount):
        student.water -= amount

    def apply_health_effects(self, student):
        # 病気になる確率に基づいて、健康状態を減らします。
        if random.random() < student.sickness_probability:
            student.current_health -= random.randint(1, 20)

        # 負傷する確率に基づいて、負傷レベルを増加させます。
        if random.random() < student.injury_probability:
            student.injury += random.randint(1, 20)

        # ストレスを増やします。
        student.stress += random.uniform(0.1, 1)

    def consume_resources(self, student, calorie_requirement, water_requirement):
        # 食べ物と水を消費します。
        self.consume_food(student, calorie_requirement)
        self.consume_water(student, water_requirement)

    def adjust_calorie_requirement(self, student):
        # 健康状態が100より低い場合、基本的なカロリー要件を追加します。
        if student.current_health < 100:
            student.base_calorie_requirement += 100

    def remove_dead_student(self, i):
        # 生存者が死亡する場合、リストから削除します。
        self.students[i].is_dead = True

    def distribute_resources(self):
        # 死亡した女生徒の人肉が最大40人に配給される(女生徒の人肉が平均して、40kg=80000kcalであると仮定)
        for j in range(min(40, len(self.students))):
            self.add_food(self.students[j], (1 + self.students[j].survival_ability) * 2000)
            self.add_water(self.students[j], (1 + self.students[j].survival_ability) * 2500)

    def run(self):
        self.reset()

        cube_indices = random.sample(range(len(self.cubes)), len(self.students))

        for index in cube_indices:
            self.open_door(index)

        alive_students = self.students

        while len(alive_students) > 1:
            for i, student in enumerate(self.students):
                calorie_requirement = student.base_calorie_requirement
                water_requirement = student.daily_water_requirement

                self.apply_health_effects(student)
                self.consume_resources(student, calorie_requirement, water_requirement)
                self.adjust_calorie_requirement(student)

                event_chance = random.random()
                if event_chance < 0.05:
                    self.remove_dead_student(i)

                if len(self.students) >= 40 and event_chance < 0.1:
                    self.distribute_resources()

                if student.food <= 0 or student.water <= 0 or student.stress >= 100:
                    self.remove_dead_student(i)
                    self.distribute_resources()

                alive_students = [
                    student for student in self.students if not student.is_dead
                ]

                print(len(alive_students))
            dead_students = [student for student in self.students if student.is_dead]
            self.days_survived += 1
        return self.opened_cubes, len(dead_students), self.days_survived
