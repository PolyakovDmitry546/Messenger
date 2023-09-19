<a name="readme-top"></a>
# Messenger

<!-- ABOUT THE PROJECT -->
## О проекте

Проект web версии мессенджера, созданный используя Django, Django REST framework, Django Channels.


<!-- GETTING STARTED -->
### Предворительные требования

Для запуска проекта вам понадобиться Python 3.11+, менеджер пакетов Poetry или можете использовать Docker.

### Установка

1. Клонируйте репозиторий и перейдите в папку проекта
   ```sh
   git clone https://github.com/PolyakovDmitry546/Messenger.git
   cd Messenger
   ```
2. Создайте виртуальное окружение и активируйте его
   ```sh
   python -m venv venv
   ```
   ```sh
   source venv/bin/activate
   ```
   или
   ```sh
   .\venv\Scripts\activate.ps1
   ```
3. Установите зависимости
   ```sh
   poetry install
   ```
4. Измените параметры подключения к используемым базам данных в файле `messenger\messenger\settings.py`
   ```py
   DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'db_name',
        'USER': 'db_user',
        'PASSWORD': 'db_password',
        'HOST': 'hostname',
        'PORT': 'port',
    },
   }
   
   CHANNEL_LAYERS = {
    "default": {
        "BACKEND": "channels_redis.core.RedisChannelLayer",
        "CONFIG": {
            "hosts": [("hostname", "port")],
        },
    },
   }
   ```
5. Запустите проект
   ```sh
   python messenger\manage.py runserver
   ```

### Установка используя Docker

1. Клонируйте репозиторий и перейдите в папку проекта
   ```sh
   git clone https://github.com/PolyakovDmitry546/Messenger.git
   cd Messenger
   ```
2. Запустите проект
   ```sh
   docker-compose up
   ```

<p align="right">(<a href="#readme-top">вернуться в начало</a>)</p>


<!-- CONTACT -->
## Контакты

Дмитрий Поляков - polyakov1803@gmail.com

Project Link: [https://github.com/PolyakovDmitry546/Messenger](https://github.com/PolyakovDmitry546/Messenger)
