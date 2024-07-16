import asyncio
import signal

from tg import TelegramInterface
from scheduler import schedule, delete_msq_queue, delete_message_worker
from configuration import logger, apl_conf


async def shutdown(incoming_signal: signal.Signals, tg: TelegramInterface, task: asyncio.Task):
    """Cleanup tasks tied to the service's shutdown."""
    logger.info(f"Received exit signal {incoming_signal.name}...")
    apl_conf.run = False
    await delete_msq_queue.join()
    tasks = [asyncio.create_task(tg.dispatcher.stop_polling()), task]
    task.cancel()
    await asyncio.gather(*tasks, return_exceptions=True)
    logger.info("All tasks cancelled")


async def main():
    apl_conf.run = True
    tg: TelegramInterface = TelegramInterface()
    bot_task = asyncio.create_task(tg.run())
    scheduler_task = asyncio.create_task(schedule(tg.bot))
    message_worker_task = asyncio.create_task(delete_message_worker(delete_msq_queue, tg.bot))
    task_list = [bot_task, scheduler_task, message_worker_task]
    loop = asyncio.get_running_loop()
    for incoming_signal in (signal.SIGHUP, signal.SIGTERM, signal.SIGINT):
        loop.add_signal_handler(
            incoming_signal, lambda: asyncio.create_task(shutdown(incoming_signal, tg, message_worker_task)))
    await asyncio.gather(*task_list, return_exceptions=True)


asyncio.run(main())
