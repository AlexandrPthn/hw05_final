### **Социальная сеть Yatube**
### Описание
Cоциальная сеть ведения постов. Блог с возможностью публикации постов, подпиской на авторов, возможностью оставлять комментарии на посты.

### Стек
![python version](https://camo.githubusercontent.com/6e7b83ff04ff922842607025b466445569c2b79e7521df5b651a0d76ff7ef71e/68747470733a2f2f696d672e736869656c64732e696f2f62616467652f507974686f6e2d332e372d677265656e) [![django version](https://camo.githubusercontent.com/3b24766753d4fce1d8876ec3a6a3f6f76814ff796af79022f9e69115f609a662/68747470733a2f2f696d672e736869656c64732e696f2f62616467652f446a616e676f2d322e322d677265656e)](https://camo.githubusercontent.com/3b24766753d4fce1d8876ec3a6a3f6f76814ff796af79022f9e69115f609a662/68747470733a2f2f696d672e736869656c64732e696f2f62616467652f446a616e676f2d322e322d677265656e) [![pillow version](https://camo.githubusercontent.com/a4603e990037d36b43920e28f0f67ee679bbaaecc9faf58851494b8838f959c7/68747470733a2f2f696d672e736869656c64732e696f2f62616467652f50696c6c6f772d382e332d677265656e)](https://camo.githubusercontent.com/a4603e990037d36b43920e28f0f67ee679bbaaecc9faf58851494b8838f959c7/68747470733a2f2f696d672e736869656c64732e696f2f62616467652f50696c6c6f772d382e332d677265656e) [![pytest version](https://camo.githubusercontent.com/f4cfb62ef31f50735a09fa9612bc5a32f6cb08bdff1fd08d1af3e162d1b9cda7/68747470733a2f2f696d672e736869656c64732e696f2f62616467652f7079746573742d362e322d677265656e)](https://camo.githubusercontent.com/f4cfb62ef31f50735a09fa9612bc5a32f6cb08bdff1fd08d1af3e162d1b9cda7/68747470733a2f2f696d672e736869656c64732e696f2f62616467652f7079746573742d362e322d677265656e) [![requests version](https://camo.githubusercontent.com/9ca7d43200b6212b4603b428a19734d31f663b5cc8d1f1b801e41723eb5c814c/68747470733a2f2f696d672e736869656c64732e696f2f62616467652f72657175657374732d322e32362d677265656e)](https://camo.githubusercontent.com/9ca7d43200b6212b4603b428a19734d31f663b5cc8d1f1b801e41723eb5c814c/68747470733a2f2f696d672e736869656c64732e696f2f62616467652f72657175657374732d322e32362d677265656e) [![sorl-thumbnail version](https://camo.githubusercontent.com/0f7f8ff7b1948f062a3c0ad49e7ed6cd03ef6eea27ffa44a76b6ddb6861067cf/68747470733a2f2f696d672e736869656c64732e696f2f62616467652f7468756d626e61696c2d31322e372d677265656e)](https://camo.githubusercontent.com/0f7f8ff7b1948f062a3c0ad49e7ed6cd03ef6eea27ffa44a76b6ddb6861067cf/68747470733a2f2f696d672e736869656c64732e696f2f62616467652f7468756d626e61696c2d31322e372d677265656e)

### Запуск проекта в dev-режиме
Инструкция ориентирована на операционную систему windows и утилиту git bash.
Для прочих инструментов используйте аналоги команд для вашего окружения.
-	Клонируйте репозиторий и перейдите в него в командной строке:
```
git clone https://github.com/AlexandrPthn/hw05_final.git
cd hw05_final
```

-	Установите и активируйте виртуальное окружение
```
python -m venv venv
source venv/Scripts/activate
```
-	Установите зависимости из файла requirements.txt
```
pip install -r requirements.txt
```
-	Выполните миграции:
```
cd yatube
python manage.py migrate
```
-	Запустите сервер, выполнив команду:
```
python manage.py runserver
```
### Доступные функции:
##### Верифицированные пользователи:
- Просмотр, публикация, удаление и редактирование своих постов;
- Просмотр информации о сообществах;
- Просмотр и публикация комментариев к постам(всем), редактирование и удаление своих комментариев;
- Подписка и просмотр постов других пользователей.

##### Анонимные пользователи:
- Просмотр постов;
- Просмотр информацию о сообществах;
- Просмотр комментариев.

### Набор доступных эндпоинтов:
- Отображение постов и публикаций (GET, POST):
```
posts/
```  
- Получение, изменение, удаление поста с соответствующим id (GET, PUT, PATCH, DELETE):
```
posts/{id}
``` 
- Получение комментариев к посту с соответствующим post_id и публикация новых комментариев(GET, POST):
``` 
posts/{post_id}/comments/
``` 
- Получение, изменение, удаление комментария с соответствующим id к посту с соответствующим post_id (GET, PUT, PATCH, DELETE):
```
posts/{post_id}/comments/{id}
```
- Получение описания зарегестрированных сообществ (GET):
```
posts/groups/ 
```
- Получение описания сообщества с соответствующим id (GET):
```
posts/groups/{id}/
``` 
- Получение информации о подписках текущего пользователя, создание новой подписки на пользователя (GET, POST):
```
posts/follow/
```