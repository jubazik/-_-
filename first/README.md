GET/POST  /api/auth/login/          - Страница входа (DRF)
GET       /api/auth/logout/         - Выход
POST      /api/token/               - Получение JWT токена
POST      /api/token/refresh/       - Обновление JWT токена  
POST      /api/register/            - Регистрация нового пользователя

GET       /api/users/               - Список всех пользователей
POST      /api/users/               - Создание пользователя (через API)
GET       /api/users/{id}/          - Данные конкретного пользователя
PUT       /api/users/{id}/          - Полное обновление пользователя
PATCH     /api/users/{id}/          - Частичное обновление
DELETE    /api/users/{id}/          - Удаление пользователя
GET       /api/users/me/            - Данные текущего пользователя ✅
POST      /api/users/{id}/set_password/ - Смена пароля (админы)
GET       /api/users/stats/         - Статистика пользователей (админы)
GET       /                         - Главная страница
GET       /api/profile/             - Страница профиля (пример)
http://127.0.0.1:8000/                 - Главная
http://127.0.0.1:8000/admin/           - Админка
http://127.0.0.1:8000/api/users/       - Список пользователей
http://127.0.0.1:8000/api/users/me/    - Мой профиль
http://127.0.0.1:8000/api/register/    - Регистрация
http://127.0.0.1:8000/api/token/       - Получить JWT токен
http://127.0.0.1:8000/api/auth/login/  - Страница входа

/admin/                             django.contrib.admin.sites.login
/api/users/                         user.views.UserViewSet
/api/users/me/                      user.views.UserViewSet
/api/register/                      user.views.UserRegistrationView
/api/token/                         rest_framework_simplejwt.views.TokenObtainPairView
/api/token/refresh/                 rest_framework_simplejwt.views.TokenRefreshView
/api/auth/login/                    rest_framework.views.login
/api/auth/logout/                   rest_framework.views.logout
/                                   user.views.home_view
✅ Проверка работы:

Главная страница: http://127.0.0.1:8000/
Регистрация: http://127.0.0.1:8000/api/register/
Логин: http://127.0.0.1:8000/api/auth/login/
JWT токен: http://127.0.0.1:8000/api/token/
Профиль: http://127.0.0.1:8000/api/users/me/
Админка: http://127.0.0.1:8000/admin/
Теперь у вас есть полная система API с аутентификацией! 🚀