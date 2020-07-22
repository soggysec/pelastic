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
        is_local = parser.getboolean('elastic','local')
        if is_local:
            host = parser.get('elastic','host')
            port = int(parser.get('elastic','port'))
            es = Elasticsearch( [{'host': host, 'port': port}] )
        else:
            cloud_id = parser.get("elastic", "id")
            elastic_username = parser.get("elastic", "username")
            elastic_password = parser.get("elastic", "password")

            es = Elasticsearch(
                cloud_id=cloud_id,
                http_auth=(elastic_username, elastic_password)
            )

    except Exception as e:
        get_logger().error(e)

    print("Successfully connected to Elastic Service")

    for workout in PelotonWorkout.list():
        # Normalize some of the data
        if hasattr(workout.metrics, "output_summary"):
            output_summary = workout.metrics.output_summary.value
        else:
            output_summary = -1
        if hasattr(workout.ride, "instructor"):
            workout_name = workout.ride.instructor.name
        else:
            workout_name = ""

        doc = {
            'workout.id': workout.id,
            'workout.fitness_discipline': workout.fitness_discipline,
            'workout.status': workout.status,
            'workout.ride.duration': workout.ride.duration,
            'workout.ride.name': workout_name,
            'workout.metrics.calories': workout.metrics.calories_summary.value,
            'workout.metrics.total_output': output_summary,
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
