from pathlib import Path
from datetime import datetime
import traceback


BASE_DIR = Path(__file__).resolve().parent.parent
LOG_DIR = BASE_DIR / "logs"
APPLICATION_LOG = LOG_DIR / "application.log"


def log_exception(context: str, exception: Exception) -> None:
    """
    Record an unexpected application exception in the runtime log.
    """

    LOG_DIR.mkdir(parents=True, exist_ok=True)

    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    with APPLICATION_LOG.open("a", encoding="utf-8") as log_file:
        log_file.write(
            f"\n[{timestamp}] {context}\n"
        )
        log_file.write(
            f"Exception: {type(exception).__name__}: {exception}\n"
        )
        log_file.write("Traceback:\n")
        log_file.write(
            traceback.format_exc()
        )
        log_file.write("\n" + "-" * 80 + "\n")


def handle_exception(context: str, exception: Exception) -> str:
    """
    Log an unexpected exception and return a user-friendly message.
    """

    log_exception(context, exception)

    return (
        "An unexpected error occurred while processing your request. "
        "Please try again."
    )