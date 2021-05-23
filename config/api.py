import logging
from src.utils.common_methods import create_app

app = create_app(__name__)
app.logger = logging.getLogger('console')
