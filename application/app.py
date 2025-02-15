from application.logger import setup_logger
from application.app_factory import create_app

app = create_app()

logger = setup_logger(__name__)
