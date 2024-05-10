from tg.lexicon.command_classes import Commands
from tg.lexicon.message_classes import Messages
from tg.lexicon.button_classes import Buttons


lex_commands: Commands = Commands()
lex_messages: Messages = Messages()
lex_buttons: Buttons = Buttons()


__all__ = (
    'lex_commands',
    'lex_messages',
    'lex_buttons'
)
