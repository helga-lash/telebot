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
        info: str
            message sent when going to view information
        works: str
            message sent when going to view works
        recordCalendar: str
            message sent when you go to select a recording date
        recordCalendarSorry: str
            message sent when the selected date is no longer available
        recordTime: str
            message sent when going to select recording time
        recordConfirm: str
            message sent when requesting confirmation of an appointment
        userName: str
            message sent when a username is requested
        userSurname: str
            message sent when a user surname is requested
        userPhone: str
            message sent when requesting a phone number
        userConfirm: str
            message sent when requesting confirmation of user data
        recordOk: str
            message sent when an entry is added
    """
    notMatch: str = 'Я Вас не понимаю.\nДля получения дополнительной информации введите /help или воспользуйтесь меню.'
    techProblems: str = 'Извините, произошел сбой системы.\nПовторите попытку позже.'
    info: str = 'Что именно Вас интересует?'
    works: str = 'Какие типы работ Вы хотели бы увидеть?'
    recordCalendar: str = 'На какой день хотите записаться?'
    recordCalendarSorry: str = ('Приносим свои извинения, но запись на {date} закрыта.\nВыберете, пожалуйста, другой '
                                'день.')
    recordTime: str = 'В какое время Вам будет удобно?'
    recordConfirm: str = 'Вы будете записаны на {day} в {tm}. Всё верно?'
    userName: str = ('Для записи на процедуру необходимо зарегистрироваться в системе.\n'
                     'Если Вы согласны введите свое имя, если нет нажмите кнопку "Нет".')
    userSurname: str = 'Введите свою фамилию.'
    userPhone: str = 'Введите номер телефона для связи с Вами в формате "79*********".'
    userConfirm: str = 'Вас зовут {surname} {name}.\nС Вами можно связаться по номеру {phone}.\nВсё верно?'
    recordOk: str = ('Ваша запись зарегистрирована, {name}.\nВам придет запрос на подтверждение записи за сутки и за '
                     'два часа за неё.\nСпасибо, что воспользовались онлайн записью!\nДля продолжения работы с ботом '
                     'воспользуйтесь командой /start.')
