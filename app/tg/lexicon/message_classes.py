from dataclasses import dataclass


@dataclass(slots=True)
class Messages:
    """
    Class describing all messages

    Arguments:
        notMatch: str
            message sent to the user when the bot did not recognize his message
        techProblems: str
            message sent to the user when technical problems occur
    """
    notMatch: str = ('Я Вас не понимаю\.\n'
                    'Для получения дополнительной информации введите /help или воспользуйтесь меню\.')
    techProblems: str = ('Извините, произошел сбой системы\.\n'
                         'Повторите попытку позже\.')
    info: str = 'Что именно Вас интересует\?'
    works: str = 'Какие типы работ Вы хотели бы увидеть\?'
