import pytz
import asyncio
import logging

from datetime import datetime
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
from apscheduler.triggers.interval import IntervalTrigger

from tasks.parser import parse_and_save


async def main():
    logging.basicConfig(level=logging.INFO)
    
    tz = pytz.timezone('Asia/Tashkent')
    scheduler = AsyncIOScheduler()

    # Schedule task to run every hour    
    scheduler.add_job(
        parse_and_save,
        CronTrigger(hour=12, minute=30, timezone=tz)
    )

    # Start the scheduler
    scheduler.start()

    # Keep the script running
    while True:
        await asyncio.sleep(10)  # Sleep to keep event loop running

if __name__ == '__main__':
    asyncio.run(main())
