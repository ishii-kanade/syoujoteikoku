class SimulationView:
    def get_num_cubes(self):
        print("Enter the number of cubes:")
        return int(input())

    def show_results(self, opened_cubes, dead_students, days_survived):
        print(f"Opened cubes: {opened_cubes}")
        print(f"Dead students: {dead_students}")
        years, days = self.days_to_years_and_days(days_survived)
        print(f"n-m=1になるまで{years}年{days}日")

    @staticmethod
    def days_to_years_and_days(days):
        years = days // 365
        leap_years = years // 4
        days -= years * 365 + leap_years
        return years, days
