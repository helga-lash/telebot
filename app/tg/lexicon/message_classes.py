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
        userOk: str
            message sent when a admin user is registered in the system
        admNotRegistered: str
            message sent when the admin is not registered in the system
        name: str
            message sent when requesting the name
        recordsWorker: str
            message sent when going to work records
        recordsWorkerCalendar: str
            message sent when going to work records calendar
        infoWorker: str
            message sent when going to work information
        addedPhoto: str
            message sent when going to work added photos
        addNotes: str
            message sent when going to work added notes
        replaceNotes: str
            message sent when going to work replace notes
        reserveTime: str
            message sent when going to work reserve time
        recordReserved: str
            message sent when going to work record reserved
        addPhotoTrends: str
            message sent when going to work add photo trends
        addPhotoNaturals: str
            message sent when going to work add photo naturals
        addPhotoReviews: str
            message sent when going to work add photo reviews
        addPhotoBulks: str
            message sent when going to work add photo bulks
        addedPhotoOk: str
            message sent when going to work added photo ok
        addPhotoNotPhoto: str
            message sent when going to work add photo not photo
        photoShow: str
            message sent when going to work photo show
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
    userNameFirst: str = ('Для продолжения необходимо зарегистрироваться в системе.\n'
                          'Если Вы согласны введите свое имя, если нет нажмите кнопку "Нет".')
    userSurname: str = 'Введите свою фамилию.'
    userPhone: str = 'Введите номер телефона для связи с Вами в формате "79*********".'
    userConfirm: str = 'Вас зовут {surname} {name}.\nС Вами можно связаться по номеру {phone}.\nВсё верно?'
    userOk: str = 'Вы зарегистрированы в системе.\nДля продолжения работы с ботом воспользуйтесь командой /start.'
    recordOk: str = ('Ваша запись зарегистрирована, {name}.\nВам придет запрос на подтверждение записи за сутки и за '
                     'два часа до неё.\nСпасибо, что воспользовались онлайн записью!\nДля продолжения работы с ботом '
                     'воспользуйтесь командой /start.')
    admNotRegistered: str = ('Вы не зарегистрированы в систем.\n'
                             'Для продолжения работы с ботом пройдите регистрацию нажав кнопку да.')
    name: str = 'Введите своё имя.'
    recordsWorker: str = 'Работа с записями.'
    recordsWorkerCalendar: str = 'Информация за какой день Вас интересует?'
    infoWorker: str = 'Работа с информацией.'
    addedPhoto: str = 'Фото в какую категорию Вы хотите добавить?'
    addNotes: str = 'Введите заметки для добавления.'
    replaceNotes: str = 'Введите заметки для замены.'
    reserveTime: str = 'Выберите время которое хотите зарезервировать.'
    recordReserved: str = 'Вы хотите зарезервировать запись на {day} в {tm}?'
    reservedOk: str = '{name}, время успешно зарезервировано.'
    addPhotoTrends: str = 'Для добавления фотографий в категорию "Тренды" загрузите от одной до трех фото.'
    addPhotoNaturals: str = 'Для добавления фотографий в категорию "Естественные" загрузите от одной до трех фото.'
    addPhotoReviews: str = 'Для добавления фотографий в категорию "Отзывы" загрузите от одной до трех фото.'
    addPhotoBulks: str = 'Для добавления фотографий в категорию "Объемы" загрузите от одной до трех фото.'
    addedPhotoOk: str = 'Фотография успешно загружена.'
    addPhotoNotPhoto: str = 'Пришлите, пожалуйста, фотографии.'
    photoShow: str = 'Нажмите "Следующие" для просмотра фото из этой же категории или выберите другое действие.'
    contactShow: str = ('Номер телефона для связи: {phone}\n'
                        'WhatsApp: {whatsapp}\n'
                        'Instagram: {instagram}\n'
                        'VK: {vk}')
    adminRecordOkNotify: str = ('Новая запись на процедуру:\n'
                                'Дата: {date}\n'
                                'Время: {time}\n'
                                'Имя: {name}\n'
                                'Фамилия: {surname}\n'
                                'Телефон: {phone}')
    confirmationDay: str = ('{name}, Вы записаны на процедуру {date} в {time}.\n'
                            'Для подтверждения записи нажмите "Да", для отмены записи нажмите "Нет".')
    adminConfirmation: str = '{name} {surname} подтвердил запись на {date} в {time}.'
    adminRecordDelete: str = '{name} {surname} отменил запись на {date} в {time}.'
