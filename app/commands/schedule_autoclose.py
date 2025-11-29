# app/commands/schedule_autoclose.py

from __future__ import annotations

import time
from datetime import datetime

import schedule

from app.commands.autoclose_overdue import autoclose_overdue_tasks


def run_job() -> None:
    """Single execution of the auto-close job."""
    now = datetime.now().isoformat(timespec="seconds")
    print(f"[{now}] Running auto-close job...")
    autoclose_overdue_tasks()
    print(f"[{now}] Job finished.")


def main() -> None:
    """
    Run a simple scheduler loop that periodically executes the auto-close job.
    """

    # Dev mode: every minute (easy to test)
    schedule.every().minute.do(run_job)

    # Production style (example):
    # schedule.every().day.at("02:00").do(run_job)

    print("Started overdue auto-close scheduler (every 1 minute). Press Ctrl+C to stop.")

    while True:
        schedule.run_pending()
        time.sleep(1)


if __name__ == "__main__":
    main()
