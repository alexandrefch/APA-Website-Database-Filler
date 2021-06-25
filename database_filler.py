import random

from database import Database
from dummy_data_generator import DummyDataGenerator


class DatabaseFiller:
    class Type:
        def __init__(self, type_id, type_name):
            self.id = type_id
            self.name = type_name

    class Structure:
        def __init__(self):
            self.id = 0
            self.name = ''
            self.type_id = 0
            self.phone_number = 0
            self.url = ''
            self.description = ''
            self.address = ''
            self.lat = ''
            self.lng = ''

    TABLE = {
        'structure_type': [],
        'activity_type': [],
        'audience_type': [],
        'place_type': [],
        'pathology': [],
        'structure': [],
    }

    @staticmethod
    def add_unique_type(table_name, type_name):
        for element in DatabaseFiller.TABLE[table_name]:
            if element.name == type_name:
                return element
        # noinspection SqlResolve
        type_id = Database.execute_insert(f'INSERT INTO {table_name} (name) VALUES (\'{type_name}\')')
        type_row = DatabaseFiller.Type(type_id, type_name)
        DatabaseFiller.TABLE[table_name].append(type_row)
        return type_row

    @staticmethod
    def fill_data(dump_info):

        structure = DatabaseFiller.Structure()
        activity_type = []
        pathology_type = []
        audience_type = []
        place_type = []

        for key, value in dump_info.items():

            if key == 'Type de structure':
                type_id = DatabaseFiller.add_unique_type('structure_type', value).id
                structure.type_id = type_id

            elif key == 'Discipline':
                for x in value:
                    type_row = DatabaseFiller.add_unique_type('activity_type', x)
                    activity_type.append(type_row)

            elif key == 'Public':
                for x in value:
                    type_row = DatabaseFiller.add_unique_type('audience_type', x)
                    audience_type.append(type_row)

            elif key == 'Lieu de pratique':
                for x in value:
                    type_row = DatabaseFiller.add_unique_type('place_type', x)
                    place_type.append(type_row)

            elif key == 'Pathologies / Prévention':
                for x in value:
                    type_row = DatabaseFiller.add_unique_type('pathology', x)
                    pathology_type.append(type_row)

            elif key == 'Téléphone de la structure':
                structure.phone_number = value

            elif key == 'URL du site internet':
                structure.url = value

            elif key == 'Contexte':
                structure.description = value

            elif key == 'address':
                structure.address = value

            elif key == 'lat':
                structure.lat = value

            elif key == 'lng':
                structure.lng = value

            elif key == 'name':
                structure.name = value

        structure.id = Database.execute_insert(
            f'INSERT INTO structure (name, type_id, phone_number, url, description, address, lat, lng)'
            'VALUES (\'{}\', {}, \'{}\', \'{}\', \'{}\', \'{}\', \'{}\', \'{}\')'.format(
                structure.name,
                structure.type_id,
                structure.phone_number,
                structure.url,
                structure.description,
                structure.address,
                structure.lat,
                structure.lng
            )
        )
        DatabaseFiller.TABLE['structure'].append(structure)

        for ac_type in activity_type:
            activity_id = Database.execute_insert(
                f'INSERT INTO activity (structure_id, description, rate, discipline_id) '
                'VALUES ({}, \'{}\', \'{}\', {})'.format(
                    structure.id,
                    'empty desc',
                    'empty rate',
                    ac_type.id
                )
            )

            for pa_type in pathology_type:
                Database.execute_insert(
                    f'INSERT INTO activity_pathology (activity_id, pathology_id) '
                    'VALUES ({}, {})'.format(
                        activity_id,
                        pa_type.id
                    )
                )

            for au_type in audience_type:
                Database.execute_insert(
                    f'INSERT INTO activity_audience_type (activity_id, audience_type_id) '
                    'VALUES ({}, {})'.format(
                        activity_id,
                        au_type.id
                    )
                )

            for pl_type in place_type:
                Database.execute_insert(
                    f'INSERT INTO activity_place_type (activity_id, place_type_id) '
                    'VALUES ({}, {})'.format(
                        activity_id,
                        pl_type.id
                    )
                )

            random_person = DummyDataGenerator.generate_person()
            person_id = Database.execute_insert(
                f'INSERT INTO person (first_name, last_name) '
                'VALUES (\'{}\', \'{}\')'.format(
                    random_person[0],
                    random_person[1]
                )
            )

            # generate dummy schedule
            for i in range(4, 7 + random.randint(0, 4)):
                schedule = DummyDataGenerator.generate_schedule()
                Database.execute_insert(
                    f'INSERT INTO schedule (contributor_id, activity_id, duration, week_day, begin) '
                    'VALUES ({}, {}, {}, {}, \'{}\')'.format(
                        person_id,
                        activity_id,
                        schedule[0],
                        schedule[1],
                        schedule[2],
                    )
                )
