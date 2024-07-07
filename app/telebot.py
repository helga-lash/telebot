import asyncio
import signal

from tg import TelegramInterface
from scheduler import schedule
from configuration import logger, apl_conf


async def shutdown(incoming_signal: signal.Signals, tg: TelegramInterface):
    """Cleanup tasks tied to the service's shutdown."""
    logger.info(f"Received exit signal {incoming_signal.name}...")
    apl_conf.run = False
    await tg.dispatcher.stop_polling()
    logger.info("Closing database connections")


async def main():
    apl_conf.run = True
    tg: TelegramInterface = TelegramInterface()
    bot_task = asyncio.create_task(tg.run())
    scheduler_task = asyncio.create_task(schedule(tg.bot))
    task_list = [bot_task, scheduler_task]
    loop = asyncio.get_running_loop()
    for incoming_signal in (signal.SIGHUP, signal.SIGTERM, signal.SIGINT):
        loop.add_signal_handler(
            incoming_signal, lambda: asyncio.create_task(shutdown(incoming_signal, tg)))
    await asyncio.gather(*task_list)


asyncio.run(main())
