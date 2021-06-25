import debug
from database import Database
from database_filler import DatabaseFiller
from html_dumper import HtmlDumper
from bs4 import BeautifulSoup
import json

URL = 'https://sport-sante-centrevaldeloire.fr'


def read_json_data(file_name):
    debug.start_subtask('Reading json file')
    file = open(file_name, 'r')
    json_data = json.load(file)
    return json_data


def database_connection(db_host, db_name, db_user, db_pass):
    debug.start_subtask('Connect to database')
    Database.connect(db_user, db_pass, db_host, db_name)


def database_clear():
    debug.start_subtask('Clearing database')
    for table in ['schedule_person', 'schedule', 'person', 'activity_pathology', 'activity_place_type',
                  'activity_audience_type', 'activity', 'structure', 'audience_type', 'activity_type',
                  'pathology', 'place_type', 'structure_type']:
        Database.execute(f'DELETE FROM {table} WHERE 1;')
    Database.commit()


def database_populate(json_data):
    debug.start_subtask('Dumping information')
    for i, data in enumerate(json_data):
        a_link = BeautifulSoup(data['link'], 'html.parser').a
        dumped_info = HtmlDumper.dump_page(URL + a_link['href'])
        name = a_link.string.replace('\'', '\\\'')
        coords = data['coords']
        lat = coords['lat']
        lng = coords['lng']
        address = data['address'].replace('\'', '\\\'')
        dumped_info.update({'lat': lat, 'lng': lng, 'address': address, 'name': name})
        DatabaseFiller.fill_data(dumped_info)
        debug.set_subtask_progression(i, len(json_data))
    debug.start_subtask('Uploading data')
    Database.commit()


def database_close():
    debug.start_subtask('Closing connection')
    Database.close()


def main():
    db_host = input('db_host=')
    db_name = input('db_name=')
    db_user = input('db_user=')
    db_pass = input('db_pass=')

    print('')

    debug.start_task('Initialisation')
    json_data = read_json_data('data/sscvl.json')
    database_connection(db_host, db_name, db_user, db_pass)
    database_clear()
    debug.end_current_task()

    debug.start_task('Exploiting json data')
    database_populate(json_data)
    database_close()
    debug.end_current_task()


if __name__ == '__main__':
    main()
