import logging
import os

from peloton import peloton, PelotonWorkout
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

    for workout in PelotonWorkout.list(limit=100):
        # Normalize some of the data
        # Rides and Runs have Distance
        distance_summary = -1
        distance_unit = ""

        # Rides have "Outputs"
        output_summary = -1
        output_unit = ""
        avg_output = -1
        avg_output_unit = ""

        # If you have an HRM, you should have HRM stats
        avg_hr = -1
        avg_hr_unit = ""

        if hasattr(workout.metrics, "distance_summary"):
            distance_summary = workout.metrics.distance_summary.value
            distance_unit = workout.metrics.distance_summary.unit

        if hasattr(workout.metrics, "output_summary"):
            # This only exists in Rides
            output_summary = workout.metrics.output_summary.value
            output_unit = workout.metrics.output_summary.unit

        if hasattr(workout.metrics, "output"):
            avg_output = workout.metrics.output.average
            avg_output_unit  = workout.metrics.output.unit

        if hasattr(workout.metrics, "heart_rate"):
            avg_hr        = workout.metrics.heart_rate.average
            avg_hr_unit  = workout.metrics.heart_rate.unit

        if hasattr(workout.ride, "instructor"):
            instructor_name = workout.ride.instructor.name
        else:
            instructor_name = ""

        best_output = False
        for achievement in workout.achievements:
            if "best_output" == achievement.slug:
                best_output = True
                break

        doc = {
            'id': workout.id,
            'username': peloton.PELOTON_USERNAME,
            'fitness_discipline': workout.fitness_discipline,
            'instructor_name': instructor_name,
            'total_output': output_summary,
            'output_unit': output_unit,
            'calories': workout.metrics.calories_summary.value,
            'duration': workout.ride.duration,
            'personal_record': best_output,

            'distance_summary': distance_summary,
            'distance_unit': distance_unit,

            'avg_output': avg_output,
            'avg_output_unit': avg_output_unit,

            'avg_hr': avg_hr,
            'avg_hr_unit': avg_hr_unit,

            'status': workout.status,
            '@timestamp': workout.created_at.strftime("%Y/%m/%d %H:%M:%S"),
            'start_time': workout.start_time.strftime("%Y/%m/%d %H:%M:%S"),
            'end_time': workout.end_time.strftime("%Y/%m/%d %H:%M:%S")
        }

        res = es.index(index="pelastic", id=workout.id, body=doc)
        print(res['result'])

if __name__ == "__main__":
    main()
