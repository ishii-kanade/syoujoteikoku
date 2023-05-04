from model.cube import Cube
from model.female_student import FemaleStudent
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

    def add_water(self, student, amount):
        student.water += amount

    def consume_food(self, student, amount):
        student.food -= amount

    def consume_water(self, student, amount):
        student.water -= amount

    def apply_health_effects(self, student):
        # 病気になる確率に基づいて、健康状態を減らします。
        if random.random() < student.sickness_probability:
            student.current_health -= random.randint(-20, 20)

        # 負傷する確率に基づいて、負傷レベルを増加させます。
        if random.random() < student.injury_probability:
            student.injury += random.randint(-20, 20)

        # ストレスを増やします。
        student.stress += random.randint(-1, 1)

    def consume_resources(self, student):
        # 食べ物と水を消費します。
        self.consume_food(student, student.base_calorie_requirement)
        self.consume_water(student, student.daily_water_requirement)

    def adjust_calorie_requirement(self, student):
        # 健康状態が100より低い場合、基本的なカロリー要件を追加します。
        if student.current_health < 100:
            student.base_calorie_requirement += 100

    def distribute_resources(self, alive_students):
        # 死亡した女生徒の人肉が最大40人に配給される(女生徒の人肉が平均して、40kg=80000kcalであると仮定)
        students_to_receive_resources = alive_students[: min(40, len(alive_students))]

        for student in students_to_receive_resources:
            self.add_food(student, (1 + student.survival_ability) * 2000)
            self.add_water(student, (1 + student.survival_ability) * 2500)

    def random_food_water_event(self, student):
        if random.random() < 0.1:
            found_food = random.randint(500, 1000)
            found_water = random.randint(500, 1500)
            self.add_food(student, found_food)
            self.add_water(student, found_water)
            print(
                f"Student found {found_food} units of food and {found_water} units of water."
            )

    def run(self):
        self.reset()

        cube_indices = random.sample(range(len(self.cubes)), len(self.students))

        for index in cube_indices:
            self.open_door(index)

        alive_students = self.students

        while len(alive_students) > 1:
            for student in alive_students:
                if student.food <= 0:
                    print("Student died due to lack of food.")
                    student.is_dead = True
                elif student.water <= 0:
                    print("Student died due to lack of water.")
                    student.is_dead = True
                elif student.stress >= 100:
                    print("Student died due to high stress.")
                    student.is_dead = True
                elif student.current_health <= 0:
                    print("Student died due to poor health.")
                    student.is_dead = True
                elif student.injury >= 100:
                    print("Student died due to severe injuries.")
                    student.is_dead = True

                if student.is_dead:
                    self.distribute_resources(alive_students)

                self.random_food_water_event(student)
                self.apply_health_effects(student)
                self.consume_resources(student)
                self.adjust_calorie_requirement(student)

                alive_students = [
                    student for student in self.students if not student.is_dead
                ]
            self.days_survived += 1
            print("Alive students: " + str(len(alive_students)))
        return (
            self.opened_cubes,
            len(self.students) - len(alive_students),
            self.days_survived,
        )
