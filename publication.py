# coding: utf-8
from datetime import datetime
from flask import Flask, make_response, render_template, Response, request, send_from_directory
import hashlib


# Default configuration
DEBUG = False

GREETINGS = { 
    'english':      ('Good morning', 'Hello', 'Good evening'), 
    'french':       ('Bonjour', 'Bonjour', 'Bonsoir'), 
    'german':       ('Guten morgen', 'Hallo', 'Guten abend'), 
    'spanish':      ('Buenos días', 'Hola', 'Buenas noches'), 
    'portuguese':   ('Bom dia', 'Olá', 'Boa noite'), 
    'italian':      ('Buongiorno', 'Ciao', 'Buonasera'), 
    'swedish':      ('God morgon', 'Hallå', 'God kväll'),
}

app = Flask(__name__, static_url_path='')
app.config.from_object(__name__)
# If there's a HELLOWORLD_SETTINGS environment variable, which should be a
# config filename, use those settings:
app.config.from_envvar('HELLOWORLD_SETTINGS', silent=True)


@app.route('/')
def root():
    return make_response('A Little Printer publication.')

@app.route('/meta.json')
@app.route('/icon.png')
def static_from_root():
    return send_from_directory(app.static_folder, request.path[1:])


# Called to generate the sample shown on BERG Cloud Remote.
#
# == Parameters:
#   None.
#
# == Returns:
# HTML/CSS edition.
#
@app.route('/sample/')
def sample():
    # The values we'll use for the sample:
    language = 'english'
    name = 'Little Printer'
    response = make_response(render_template(
                        'edition.html',
                        greeting="%s, %s" % (GREETINGS[language][0], name),
                    ))
    response.headers['Content-Type'] = 'text/html; charset=utf-8'
    # Set the ETag to match the content.
    response.headers['ETag'] = '"%s"' % (
        hashlib.md5(
            language + name + datetime.utcnow().strftime('%d%m%Y')
        ).hexdigest()
    )
    return response

if __name__ == '__main__':
    app.debug = app.config['DEBUG']
    app.run()
