from flask import url_for
from flask_migrate import MigrateCommand
from flask_script import Manager
from urllib.parse import urlparse
from app import app

manager = Manager(app)

# Database migrations command
manager.add_command('db', MigrateCommand)

@manager.command
def list_routes():
    import urllib
    output = []
    for rule in app.url_map.iter_rules():

        options = {}
        for arg in rule.arguments:
            options[arg] = "[{0}]".format(arg)

        methods = ','.join(rule.methods)
        url = url_for(rule.endpoint, **options)
        line = urlparse("{:50s} {:20s} {}".format(rule.endpoint, methods, url))
        output.append(line)

    for line in sorted(output):
        print(line)


if __name__ == '__main__':
    manager.run()
