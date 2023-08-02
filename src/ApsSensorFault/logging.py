import os
import sys
import logging
from datetime import datetime

LOG_FILE = f"{datetime.now().strftime('%M_%d_%Y_%H_%M_%S')}.log"
log_dir = 'logs'
log_path = os.path.join(log_dir, LOG_FILE)

logging_str = "[%(asctime)s: %(levelname)s: %(module)s]: %(message)s"
os.makedirs(log_dir, exist_ok=True)

logging.basicConfig(
    level=logging.INFO,
    format=logging_str,
    handlers=[
        logging.FileHandler(log_path),
        logging.StreamHandler(sys.stdout)
    ]
)

log = logging.getLogger("ApsSensorFault")