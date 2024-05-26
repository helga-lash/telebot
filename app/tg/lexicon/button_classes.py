from dataclasses import dataclass, field


@dataclass(slots=True)
class Button:
    """
    Class describing button entity

    Arguments:
        text: str
            text written on the button
        callback: str
            callback returned by the button
    """
    text: str
    callback: str


@dataclass(slots=True)
class Buttons:
    """
    Class describing all buttons

    Arguments:
        record: Button
            button to register for the procedure
        info: Button
            button to view information
        works: Button
            button to view works
        reviews: Button
            button to view reviews
        contacts: Button
            button to view contacts
        trends: Button
            button to view trends
        naturals: Button
            button to view naturals
        bulks: Button
            button to view bulks
        next: Button
            button to view next photos
        yes: Button
            positive answer button
        no: Button
            negative answer button
    """
    record: Button = field(default_factory=lambda: Button(
        text='Запись',
        callback='record'
    )
                           )
    info: Button = field(default_factory=lambda: Button(
        text='Информация',
        callback='info'
    )
                           )
    works: Button = field(default_factory=lambda: Button(
        text='Работы',
        callback='works'
    )
                          )
    reviews: Button = field(default_factory=lambda: Button(
        text='Отзывы',
        callback='reviews'
    )
                          )
    contacts: Button = field(default_factory=lambda: Button(
        text='Контакты',
        callback='contacts'
    )
                          )
    trends: Button = field(default_factory=lambda: Button(
        text='Тренды',
        callback='trends'
    )
                             )
    naturals: Button = field(default_factory=lambda: Button(
        text='Естественные',
        callback='naturals'
    )
                             )
    bulks: Button = field(default_factory=lambda: Button(
        text='Объемы',
        callback='bulks'
    )
                             )
    next: Button = field(default_factory=lambda: Button(
        text='Следующие',
        callback='next'
    )
                             )
    yes: Button = field(default_factory=lambda: Button(
        text='Да',
        callback='yes'
    )
                             )
    no: Button = field(default_factory=lambda: Button(
        text='Нет',
        callback='no'
    )
                        )
    recordsView: Button = field(default_factory=lambda: Button(
        text='Просмотр записей',
        callback='recordsView'
    )
                                )
    timeReserve: Button = field(default_factory=lambda: Button(
        text='Зарезервировать время',
        callback='timeReserve'
    )
                                )
    addedPhoto: Button = field(default_factory=lambda: Button(
        text='Добавить фото',
        callback='addedPhoto'
    )
                               )
    changeContact: Button = field(default_factory=lambda: Button(
        text='Изменить контакты',
        callback='changeContact'
    )
                                  )
