from config import config
from app import create_app
import os


get_config_mode = os.environ.get('FLASK_CONFIG', 'Debug').capitalize()
app_config = config[get_config_mode]
app = create_app(get_config_mode)

app.logger.info('Environment = ' + get_config_mode)

if __name__ == "__main__":
    app.run()
