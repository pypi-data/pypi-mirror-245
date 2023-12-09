import logging
logging.basicConfig(
    level=logging.WARNING,  # Set the desired logging level
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

LOGGER = logging.getLogger(__name__)

from .Client import Client
