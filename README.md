# yamdb_final


Проект **YaMDb** собирает отзывы пользователей на произведения.

Произведения делятся на категории: «Книги», «Фильмы», «Музыка».

Запросы к API начинаются с '/api/v1/'

### Алгоритм регистрации пользователей
1. Пользователь отправляет запрос с параметром `email` на `/auth/email/`.
2. **YaMDB** отправляет письмо с кодом подтверждения (`confirmation_code`) на адрес  `email` .
3. Пользователь отправляет запрос с параметрами `email` и `confirmation_code` на `/auth/token/`, в ответе на запрос ему приходит `token` (JWT-токен).
4. При желании пользователь отправляет PATCH-запрос на `/users/me/` и заполняет поля в своём профайле (описание полей — в документации).
### Пользовательские роли
- **Аноним** — может просматривать описания произведений, читать отзывы и комментарии.
- **Аутентифицированный пользователь** — может, как и **Аноним**, читать всё, дополнительно он может публиковать отзывы и ставить рейтинг произведениям (фильмам/книгам/песенкам), может комментировать чужие отзывы и ставить им оценки; может редактировать и удалять **свои** отзывы и комментарии.
- **Модератор** — те же права, что и у **Аутентифицированного пользователя** плюс право удалять **любые** отзывы и комментарии.
- **Администратор** — полные права на управление проектом и всем его содержимым. Может создавать и удалять категории и произведения. Может назначать роли пользователям.
- **Администратор Django** — те же права, что и у роли **Администратор**.

[Полная документация](https://github.com/ant-willow/yamdb_final/blob/master/static/redoc.yaml)

## Инструкция для развертывания:
 - Клонировать себе репозиторий
 - Заполнить секреты в репозитории:\
	 **USER** - имя пользователя для подключения к серверу\
	 **HOST** - IP-адрес сервера\
	 **SSH_KEY** - приватный ключ\
	 **PASSPHRASE** - фраза-пароль для ключа\
	 **DOCKER_USERNAME** - имя пользователя Docker Hub\
	 **DOCKER_PASSWORD** - пароль от Docker Hub\
	 **TELEGRAM_TO** - id чата в Telegram\
	 **TELEGRAM_TOKEN** - токен бота Telegram\
	 **SECRET_KEY** - секретный ключ Django\
	 **POSTGRES_PASSWORD** - пароль от базы
 - Сделать push

После удачного запуска, проект будет доступен по адресу HOST.