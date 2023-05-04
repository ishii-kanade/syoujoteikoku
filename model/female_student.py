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
        self.is_dead = False
        self.max_food = 10000  # 食料の最大値
        self.max_water = 5000  # 水の最大値
