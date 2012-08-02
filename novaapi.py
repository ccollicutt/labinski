from novaclient.v1_1 import client
from settings import *
from openstackrc import *


# Create a nova connection
nova = client.Client(OS_USERNAME, OS_PASSWORD, OS_TENANT_NAME, OS_AUTH_URL, service_type="compute")

