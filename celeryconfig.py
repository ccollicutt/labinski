# Celery
BROKER_URL = "amqp://guest:guest@localhost:5672//"
CELERY_RESULT_BACKEND = "database"
CELERY_RESULT_DBURI = "postgresql://celery:celery@localhost/celery"
CELERY_IMPORTS = ("tasks", )
#CELERY_RESULT_ENGINE_OPTIONS = {"echo": True}
CELERY_TASK_SERIALIZER = "pickle"
CELERY_ANNOTATIONS = {"tasks.add": {"rate_limit": "10/s"}}