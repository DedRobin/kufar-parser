import logging
import os

# URL and Token
URL = "https://www.kufar.by/l/r~minsk/noutbuki/nb~apple?cmp=0&cnd=1&sort=lst.d"
BOT_TOKEN = os.environ.get("BOT_TOKEN", None)

# Filter
DAYS_AGO = 1

# Cache limit
LIMIT_OF_RECORDS = 500

# Logger
logger = logging.getLogger(__name__)
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
