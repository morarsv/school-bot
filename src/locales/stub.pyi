from typing import Literal

    
class TranslatorRunner:
    def get(self, path: str, **kwargs) -> str: ...
    
    admin: Admin
    registration: Registration
    my: My
    hero: Hero
    err: Err
    ur: Ur
    lvl: Lvl
    max: Max
    coins: Coins
    btn: Btn


class Admin:
    panel: AdminPanel
    msg: AdminMsg


class AdminPanel:
    list: AdminPanelList
    input: AdminPanelInput
    info: AdminPanelInfo

    @staticmethod
    def menu() -> Literal["""Ты админ 👑!
Какой функционал доступен.

🔹 &lt;b&gt;Список героев 📜&lt;/b&gt; — предоставляет список всех учеников для просмотра.

🔹 &lt;b&gt;➕ Начислить/➖Списать&lt;/b&gt; — Начислить или списать коины у группы учеников.

🔹 &lt;b&gt;➕ Начислить коины&lt;/b&gt; — Начислить введенную сумму у группы учеников.

🔹 &lt;b&gt;📢 Написать всем&lt;/b&gt; — Написать всем пользователям.

🔹 &lt;b&gt;🏆 Рейтинг&lt;/b&gt; — Best of 30!"""]: ...


class AdminPanelList:
    fill: AdminPanelListFill
    empty: AdminPanelListEmpty

    @staticmethod
    def heroes() -> Literal["""Для просмотра определенного ученика, выбери его из списка."""]: ...


class AdminPanelInput:
    accrual: AdminPanelInputAccrual

    @staticmethod
    def usernames() -> Literal["""Введи список ников через запятую. Регистр важен.
&lt;i&gt;Прим.: Thorn_Elf, Борисыч9, ZaraDark &lt;/i&gt;"""]: ...

    @staticmethod
    def msg() -> Literal["""Введи текст сообщения, которое будет отправлено всем ученикам."""]: ...

    @staticmethod
    def summ() -> Literal["""Введи сумму для списания."""]: ...


class AdminPanelListFill:
    @staticmethod
    def usernames() -> Literal["""Вот список найденных учеников. И только тебе решать что с ними делать.

🔹 &lt;b&gt;➕ Начислить&lt;/b&gt; — всем: +20 XP и коины по формуле

🔹 &lt;b&gt;➖ Списать&lt;/b&gt; — вводится сумма, списывается у всех введённых"""]: ...


class AdminPanelListEmpty:
    @staticmethod
    def usernames() -> Literal["""Увы, но мне не удалось найти учеников. Проверь правильность ников."""]: ...


class AdminPanelInputAccrual:
    @staticmethod
    def summ(*, users) -> Literal["""Найденные ученики: { $users }

Введите количество коинов для начисления."""]: ...


class AdminMsg:
    lessons: AdminMsgLessons
    daily: AdminMsgDaily

    @staticmethod
    def accrual(*, coins) -> Literal["""Тебе начислено за урок &lt;b&gt;{ $coins } коинов!&lt;/b&gt; 💰"""]: ...

    @staticmethod
    def debt(*, coins) -> Literal["""У тебя списано &lt;b&gt;{ $coins } коинов!&lt;/b&gt; 💰"""]: ...


class AdminMsgLessons:
    @staticmethod
    def accrual(*, coins) -> Literal["""Тебе начислено за урок &lt;b&gt;20 XP и { $coins } коинов!&lt;/b&gt; 💰"""]: ...


class AdminMsgDaily:
    @staticmethod
    def rewards(*, coins) -> Literal["""Ты получил ежедневную награду: 20 XP и { $coins } коинов!📖✨"""]: ...


class AdminPanelInfo:
    @staticmethod
    def hero(*, h_class, h_name, lvl, xp, progress, coins, school_stars, reward) -> Literal["""&lt;b&gt;{ $h_class } ({ $h_name })&lt;/b&gt;
🔼 Уровень: { $lvl }
✨ Опыт: { $xp }
{ $progress }

💰 Коины: { $coins }
🏫 Уровень школы: { $school_stars }

➕ За урок: +20 XP и { $reward } коин 💰"""]: ...


class Registration:
    hero: RegistrationHero

    @staticmethod
    def preview() -> Literal["""Привет!
Добро пожаловать в учебное приключение 🎮
Здесь знания приносят награды, а герои растут вместе с тобой.

🔹 Выбери себе героя: рыцарь, гном, эльф, фея или волшебник.
🔹 Затем придумай себе имя — это будет твой никнейм.
🔹 Проходи уроки, зарабатывай коины и опыт, прокачивайся и открывай награды!

Начнём с героя — кем ты  будешь в игре?"""]: ...

    @staticmethod
    def name() -> Literal["""Придумай себе имя 🦊

Это будет твой игровой ник — его будут видеть другие.
Тебе нужно придумать ник на русском языке, от 4 до 20 символов.
Цифры и подчёркивания — тоже разрешены.

Вот несколько примеров для вдохновения:

🔹 &lt;i&gt;Алексей007&lt;/i&gt;
🔹 &lt;i&gt;Гром_Лис&lt;/i&gt;
🔹 &lt;i&gt;Анна_Фея&lt;/i&gt;
🔹 &lt;i&gt;Паша_Пират&lt;/i&gt;

⚠️Очень важно: Ник не должен содержать оскорбительных слов и цифр, иначе коины начисляться не будут.

Как назовём твоего лиса? 🥷"""]: ...


class RegistrationHero:
    @staticmethod
    def fighter() -> Literal["""Гном Лис ⛏ - Настойчивый мастер. Шаг за шагом строит фундамент знаний."""]: ...

    @staticmethod
    def knight() -> Literal["""Рыцарь Лис🛡 - Смелый защитник знаний. Он всегда готов сражаться с ленью и скукой."""]: ...

    @staticmethod
    def ranger() -> Literal["""Эльф Лиса 🏹 - Быстрая и мудрая. Помогает точно попадать в цель и быстро мыслить."""]: ...

    @staticmethod
    def sorcerer() -> Literal["""Волшебник Лис 🔮 - Хранитель великих тайн. Открывает секреты и прокачивает интеллект."""]: ...

    @staticmethod
    def wizard() -> Literal["""Фея Лиса 🧚 - Волшебница вдохновения. Превращает занятия в сказочные приключения."""]: ...


class My:
    hero: MyHero


class MyHero:
    @staticmethod
    def preview(*, h_class, h_name, lvl, xp, progress, coins, school_stars, reward) -> Literal["""&lt;b&gt;{ $h_class } ({ $h_name })&lt;/b&gt;
🔼 Уровень: { $lvl }
✨ Опыт: { $xp }
{ $progress }

💰 Коины: { $coins }
🏫 Уровень школы: { $school_stars }

➕ За урок: +20 XP и { $reward } коин 💰"""]: ...

    @staticmethod
    def school(*, school_stars, cost) -> Literal["""🏫 Магическая школа Лисхолл
Здесь обучаются самые отважные и хитрые лисы, чтобы стать мастерами своего дела.
Каждый новый уровень школы — это не просто престиж, но и бонус к награде за уроки. Чем выше твой ранг, тем больше опыта и коинов ты получаешь!

Прокачивай школу — и знания станут ещё ценнее. 📚✨

🏫 Уровень школы: { $school_stars }
💰 Стоимость прокачки: { $cost } коинов"""]: ...

    @staticmethod
    def rating(*, heroes) -> Literal["""🏆 Топ-30 игроков:

{ $heroes }"""]: ...


class Hero:
    id: HeroId

    @staticmethod
    def fighter() -> Literal["""⛏ Гном Лис"""]: ...

    @staticmethod
    def knight() -> Literal["""🛡 Рыцарь Лис"""]: ...

    @staticmethod
    def wizard() -> Literal["""🧚 Фея Лиса"""]: ...

    @staticmethod
    def ranger() -> Literal["""🏹 Эльф Лиса"""]: ...

    @staticmethod
    def sorcerer() -> Literal["""🔮 Волшебник Лис"""]: ...


class HeroId:
    @staticmethod
    def fighter() -> Literal["""fighter"""]: ...

    @staticmethod
    def knight() -> Literal["""knight"""]: ...

    @staticmethod
    def wizard() -> Literal["""wizard"""]: ...

    @staticmethod
    def ranger() -> Literal["""ranger"""]: ...

    @staticmethod
    def sorcerer() -> Literal["""sorcerer"""]: ...


class Err:
    add: ErrAdd
    input: ErrInput


class ErrAdd:
    @staticmethod
    def hero() -> Literal["""Ошибка при создании героя. Обратись к преподавателю."""]: ...


class ErrInput:
    @staticmethod
    def name() -> Literal["""Хм... Попробуй другой ник 🦊

Возможно, такое имя уже занято — или оно слишком короткое (меньше 4 символов) или длинное (больше 20).
Ник может содержать буквы на русском языке, цифры и подчёркивания.

Попробуй немного изменить его — добавь число, символ или выбери новый образ!

Например:
🔹 &lt;i&gt;Алексей007&lt;/i&gt;
🔹 &lt;i&gt;Гром_Лис&lt;/i&gt;
🔹 &lt;i&gt;Анна_Фея&lt;/i&gt;
🔹 &lt;i&gt;Паша_Пират&lt;/i&gt;

Введи новый никнейм ✍️"""]: ...

    @staticmethod
    def summ() -> Literal["""Ожидаю на вход только числа, ни каких букв!"""]: ...


class Ur:
    reward: UrReward


class UrReward:
    @staticmethod
    def coins(*, coins) -> Literal["""Твоя награда сегодня { $coins } коинов!"""]: ...

    @staticmethod
    def xp(*, xp) -> Literal["""Твоя награда сегодня { $xp } опыта!"""]: ...

    @staticmethod
    def none() -> Literal["""Сегодня тебе ничего не выпало. Попробуй завтра!"""]: ...


class Lvl:
    @staticmethod
    def up(*, lvl) -> Literal["""Уровень повышен! Теперь у тебя уровень { $lvl }!"""]: ...

    @staticmethod
    def hero(*, lvl) -> Literal["""Уровень { $lvl }"""]: ...


class Max:
    lvl: MaxLvl


class MaxLvl:
    @staticmethod
    def school() -> Literal["""Школа уже максимального уровня, и не требует"""]: ...


class Coins:
    @staticmethod
    def lessons(*, coins) -> Literal["""💰 { $coins } за урок"""]: ...


class Btn:
    daily: BtnDaily
    upgrade: BtnUpgrade
    coins: BtnCoins
    write: BtnWrite
    list: BtnList
    settings: BtnSettings

    @staticmethod
    def next() -> Literal["""Далее ➡️"""]: ...

    @staticmethod
    def back() -> Literal["""⬅️ Назад"""]: ...

    @staticmethod
    def school() -> Literal["""🏫 Школа"""]: ...

    @staticmethod
    def rating() -> Literal["""🏆 Рейтинг"""]: ...

    @staticmethod
    def accrual() -> Literal["""➕ Начислить"""]: ...

    @staticmethod
    def confirm() -> Literal["""✅ Подтвердить"""]: ...

    @staticmethod
    def cancel() -> Literal["""Отменить"""]: ...

    @staticmethod
    def update() -> Literal["""Обновить"""]: ...


class BtnDaily:
    @staticmethod
    def reward() -> Literal["""🎁 Получить награду дня"""]: ...


class BtnUpgrade:
    @staticmethod
    def school() -> Literal["""⭐️ Прокачать школу"""]: ...


class BtnCoins:
    @staticmethod
    def accrual() -> Literal["""➕ Начислить коины"""]: ...


class BtnWrite:
    @staticmethod
    def off() -> Literal["""➖ Списать"""]: ...

    @staticmethod
    def everyone() -> Literal["""📢 Написать всем"""]: ...


class BtnList:
    @staticmethod
    def heroes() -> Literal["""Список героев 📜"""]: ...


class BtnSettings:
    @staticmethod
    def heroes() -> Literal["""➕ Начислить/➖Списать"""]: ...

