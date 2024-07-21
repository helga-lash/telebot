import asyncio

from aiogram import Bot
from aiogram.types import Message

from configuration import logger, apl_conf


delete_msq_queue: asyncio.Queue[Message] = asyncio.Queue()


async def delete_message(message: Message, bot: Bot, delay: int):
    """
    Asynchronous function to delete a message after a specified delay.

    :param message: The message object to be deleted.
    :type message: aiogram.types.Message
    :param bot: The bot object used to delete the message.
    :type bot: aiogram.Bot
    :param delay: The delay in seconds before the message is deleted.
    :type delay: int
    """
    await asyncio.sleep(delay)
    try:
        await bot.delete_message(message.chat.id, message.message_id)
    except Exception as error:
        logger.error(f"Error deleting message: {error}")


async def delete_message_worker(queue: asyncio.Queue, bot: Bot):
    """
    Asynchronous function to process messages in a queue and delete them after a specified delay.

    :param queue: The queue of messages to be deleted.
    :type queue: asyncio.Queue
    :param bot: The bot object used to delete the messages.
    :type bot: aiogram.Bot
    """
    tasks: [asyncio.Task] = []
    while apl_conf.run:
        message = await queue.get()
        logger.debug(f'Adding message to delete queue: {message.message_id}')
        tasks.append(asyncio.create_task(delete_message(message, bot, 86400)))
        queue.task_done()
        for task in tasks:
            if task.done():
                logger.debug(f'Task done: {task.get_name()}')
                tasks.remove(task)
    while not queue.empty():
        message: Message = await queue.get()
        logger.debug(f'Deleting message: {message.message_id}')
        try:
            await bot.delete_message(message.chat.id, message.message_id)
        except Exception as error:
            logger.error(f"Error deleting message: {error}")
        queue.task_done()
    for task in tasks:
        if not task.done():
            logger.debug(f'Cancelling task: {task.get_name()}')
            task.cancel()
    logger.debug('All tasks cancelled')
    await asyncio.gather(*tasks)


__all__ = (
    'delete_message_worker',
    'delete_msq_queue'
)
