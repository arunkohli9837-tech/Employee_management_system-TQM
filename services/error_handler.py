"""Centralized application error logging and user-safe messages."""
from datetime import datetime
from pathlib import Path
import traceback

BASE_DIR = Path(__file__).resolve().parent.parent
LOG_DIR = BASE_DIR / "logs"
APPLICATION_LOG = LOG_DIR / "application.log"


def log_exception(context: str, exception: Exception) -> None:
    """Write diagnostic details when possible without masking the original error."""
    try:
        LOG_DIR.mkdir(parents=True, exist_ok=True)
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        trace = "".join(
            traceback.format_exception(
                type(exception), exception, exception.__traceback__
            )
        )
        with APPLICATION_LOG.open("a", encoding="utf-8") as log_file:
            log_file.write(f"\n[{timestamp}] {context}\n")
            log_file.write(f"Exception: {type(exception).__name__}: {exception}\n")
            log_file.write("Traceback:\n")
            log_file.write(trace)
            log_file.write("\n" + "-" * 80 + "\n")
    except Exception:
        # Logging must never replace the original application failure.
        # Do not print exception details here: they may contain sensitive data.
        return


def handle_exception(context: str, exception: Exception) -> str:
    """Log an exception and return a non-technical message for the UI."""
    log_exception(context, exception)
    return "An unexpected error occurred while processing your request. Please try again."
