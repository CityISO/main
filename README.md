# Образ города

## Цель
Создать веб-платформу, с помощью которой можно отслеживать настроение жителей города путем семантического анализа текста, хэштегов и эмоциональной окраски фотографии в социальных сетях.

## Схема работы
 - Парсинг данных из разных источников
 - Обработка данных
 - Проведение анализа

Это первый этап. На этом этапе мы собираем данные из социальных сетей для анализа. В ходе разработки наша команда выбрала для начала соц. сеть Instagram. Для работы с социальной сетью была выбрана библиотека [Instaloader](https://instaloader.github.io/).

Изначально, чтобы набрать данные, было собрано ~2000 постов. После этого парсинг был поставлен в фоновую задачу, чтобы постоянно обновлять данные (не более 100 постов по локации). Выполнение фоновых задач осуществляется через Celery. Данные сохраняются в PostgreSQL.

## Обработка данных
После сбора данные необходимо обработать. Для MVP было выбрано несколько направлений - обработка текста, тематическое моделирование, а также анализ фотографий.

Обработка текста проходит в несколько этапов: форматирование текста через регулярное выражение, а после все слова в тексте приводятся в начальную форму с помощью [pymorphy2](https://pymorphy2.readthedocs.io). Это делается для наивной проверки на рекламные сообщения, т.е через стоп-слова.

Исходный текст проходит тональный анализ через [NLTK](https://www.nltk.org/). Здесь возникает проблема с тем, что NLTK действует лишь для англоязычных текстов, однако это легко исправить, воспользовавшись API для работы с [GoogleTranslator](https://cloud.google.com/translate/docs/apis). В связи с необходимостью его использования, для устранения ошибок при выполнении программы, используется функция удаления смайликов из текста, базирующаяся на библиотеке [emoji](https://pypi.org/project/emoji/). Результат анализа записывается в базу данных.

Для тематического анлаиза текста наша команда использовала библиотеку [rutermextract](https://github.com/igor-shevchenko/rutermextract).

А для анализа фото была использована библиотека [keras](https://github.com/keras-team).

## Отображение данных
После обработки данных, их необходимо предоставить пользователю платформы.

Для этого был выбран WEB фреймворк Django. Это обусловлено несколькими причинами: проект легко расширяется (поскольку представляется многомодульным, мы решили взять именно Django, а не Flask), интеграция с Celery (при добавлении новой локации, нужно просто добавить задачу, аргументом которой будет ID локации), легкость добавления представлений для работы API, основной язык разработки проекта - Python.

Для работы на клиентской стороне выбран JS (VueJS и библиотеки, для работы с картой, графиками).

> Проект "Образ города" был подготовлен в ходе участия в конкурсе "Большие вызовы".
