import logging
import os

from peloton import PelotonWorkout
from elasticsearch import Elasticsearch

def get_logger():
    """ To change log level from calling code, use something like
        logging.getLogger("pelastic").setLevel(logging.DEBUG)
    """
    logger = logging.getLogger("pelastic")
    if not logger.handlers:
        handler = logging.StreamHandler()
        formatter = logging.Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]')
        handler.setFormatter(formatter)
        logger.addHandler(handler)

    return logger


def main():

    try:
        import configparser
        parser = configparser.ConfigParser()
        conf_path = os.environ.get("PELASTIC_CONFIG", "~/.config/pelastic.ini")
        parser.read(os.path.expanduser(conf_path))

        # Mandatory credentials
        cloud_id = parser.get("elastic", "id")
        elastic_username = parser.get("elastic", "username")
        elastic_password = parser.get("elastic", "password")

        es = Elasticsearch(
            cloud_id=cloud_id,
            http_auth=(elastic_username, elastic_password)
        )

    except Exception as e:
        get_logger().error("No `id`, `username`, or `password` found in section `elastic` in " + conf_path + "\n"
                           "Please ensure you specify one prior to running the program\n")

    for workout in PelotonWorkout.list():
        doc = {
            'workout.id': workout.id,
            'workout.fitness_discipline': workout.fitness_discipline,
            'workout.status': workout.status,
            'workout.ride.description': workout.ride.description,
            '@timestamp': str(workout.created_at.year) + "/" + str(workout.created_at.strftime("%m")) + "/" + str(workout.created_at.strftime("%d")) + " "
                          + str(workout.created_at.strftime("%H")) + ":" + str(workout.created_at.strftime("%M")) + ":" + str(workout.created_at.strftime("%S")),
            'workout.start_time': str(workout.start_time.year) + "/" + str(workout.start_time.strftime("%m")) + "/" + str(workout.start_time.strftime("%d")) + " "
                          + str(workout.start_time.strftime("%H")) + ":" + str(workout.start_time.strftime("%M")) + ":" + str(workout.start_time.strftime("%S")),
            'workout.end_time': str(workout.end_time.year) + "/" + str(workout.end_time.strftime("%m")) + "/" + str(workout.end_time.strftime("%d")) + " "
                        + str(workout.end_time.strftime("%H")) + ":" + str(workout.end_time.strftime("%M")) + ":" + str(workout.end_time.strftime("%S"))
        }
        res = es.index(index="pelastic", id=workout.id, body=doc)
        print(res['result'])

if __name__ == "__main__":
    main()
