import asyncio
import logging
from datetime import datetime
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger

from tasks.maxcom import parse_maxcom_product
from tasks.pcmarket import parse_pcmarket_category, parse_pcmarket_product
from tasks.ikarvon import parse_ikarvon_category, parse_ikarvon_product


async def main():
    logging.basicConfig(level=logging.INFO)

    # Initialize scheduler
    scheduler = AsyncIOScheduler()

    # Schedule task to run every hour    
    scheduler.add_job(
        parse_pcmarket_product,
        CronTrigger(hour='*/2')  # Executes every 2 hour
    )
    
    scheduler.add_job(
        parse_ikarvon_product,
        CronTrigger(hour='*/2')  # Executes every 2 hour
    )

    scheduler.add_job(
        parse_maxcom_product,
        CronTrigger(hour='*/2')  # Executes every 2 hour
    )

    # Start the scheduler
    scheduler.start()

    # Keep the script running
    while True:
        await asyncio.sleep(10)  # Sleep to keep event loop running

if __name__ == '__main__':
    asyncio.run(main())
