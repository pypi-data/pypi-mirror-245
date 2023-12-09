import os

def get_smart_ui_server_address():
    return os.getenv('SMARTUI_SERVER_ADDRESS', 'http://localhost:8080')

def get_pkg_name():
    return "@lambdatest/python-selenium-driver"