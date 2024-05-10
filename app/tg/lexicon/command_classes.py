from dataclasses import dataclass, field


@dataclass(slots=True)
class Command:
    """
    Class describing command entity

    Arguments:
        command: str
            command in telegram
        descr: str
            command description
        msg: str
            message sent to the user after the command is executed
    """
    command: str
    descr: str
    msg: str


@dataclass(slots=True)
class Commands:
    """
    Class describing all commands

    Arguments:
        start: Command
            telegram start command
        help: Command
            telegram help command
    """
    start: Command = field(default_factory=lambda: Command(
        command='start',
        descr='Начать работу',
        msg='Здравствуйте{name}\!\nЧем могу помочь\?')
                           )
    help: Command = field(default_factory=lambda: Command(
        command='help',
        descr='Информация',
        msg='Здесь вы можете получить информацию обо мне и записаться на процедуру\.\nДля начала работы введите /start '
            'или воспользуйтесь меню\.')
                          )
