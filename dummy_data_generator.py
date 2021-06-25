import random


class DummyDataGenerator:
    lastname = []
    firstname = []

    @staticmethod
    def load():
        file = open('./data/prénom.txt', 'r', encoding='utf-8')
        DummyDataGenerator.firstname = file.readlines()
        file.close()

        file = open('./data/patronyme.txt', 'r', encoding='utf-8')
        DummyDataGenerator.lastname = file.readlines()
        file.close()

    @staticmethod
    def generate_person():
        if len(DummyDataGenerator.lastname) == 0:
            DummyDataGenerator.load()

        return \
            DummyDataGenerator.firstname[random.randint(0, len(DummyDataGenerator.firstname)-1)].strip(),\
            DummyDataGenerator.lastname[random.randint(0, len(DummyDataGenerator.lastname)-1)].strip()

    @staticmethod
    def generate_schedule():
        week_day = random.randint(0, 6)
        duration = random.randint(20, 120)
        begin = random.randint(1, 48) * 15

        delta = begin + 7 * 60 + duration - 20 * 60
        if delta > 0:
            begin -= delta

        begin_hour = begin // 60
        begin_min = begin - begin_hour * 60

        return duration, week_day, f'{(begin_hour+7)}:{begin_min}:00'
