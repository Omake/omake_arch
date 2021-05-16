from wsgiref.simple_server import make_server
from omake_framework.main import Framework
from omake_framework.front_controller import fronts_list
from views import route_list


server_application = Framework(route_list, fronts_list)


with make_server('', 8000, server_application) as server:
    print('ON AIR')
    server.serve_forever()
