authors_api_spec_delete = {
    "description": "Delete the author and all their books",
    "tags": ["authors"],
    "parameters": [
        {
            "in": "path",
            "name": "id",
            "type": "integer",
            "required": True,
            "description": "ID of the author",
        }
    ],
    "responses": {200: {"description": "Author and all their books deleted"}},
}

index_spec = {
    "description": "Стартовая страница единственного шаблона index.html",
    "tags": ["index"],
    "parameters": [
        {
            "in": "header",
            "name": "Api-key",
            "type": "string",
            "required": True,
            "description": "Api-key of the user",
        }
    ],
    "responses": {200: {"description": "index template"}},
}

get_users_me_spec = {
    "description": "Страница с информацией о юзере",
    "tags": ["get_user_me"],
    "parameters": [
        {
            "in": "header",
            "name": "Api-key",
            "type": "string",
            "required": True,
            "description": "Api-key of the user",
        }
    ],
    "responses": {
        200: {
            "description": "Информация о юзере",
            "content": {
                "application/json": {
                    "example": {
                        "result": "true",
                        "user": {
                            "id": 1,
                            "name": "John Doe",
                            "followers": [
                                {"id": 2, "name": "Follower Name"}
                            ],
                            "following": [
                                {"id": 3, "name": "Following Name"}
                            ]}}}}}}}

get_users_id_spec = {
    "description": "Страница с подписчиками и на кого подписан",
    "tags": ["get_user_id"],
    "parameters": [
        {
            "in": "path",
            "name": "id",
            "type": "int",
            "required": True,
            "description": "target id user",
        }
    ],
    "responses": {
        200: {
            "description": "Показывает подписчиков и на кого подписан целевой юзер",
            "content": {
                "application/json": {
                    "example": {
                        "result": "true",
                        "user": {
                            "id": 1,
                            "name": "John Doe",
                            "followers": [
                                {"id": 2, "name": "Follower Name"}
                            ],
                            "following": [
                                {"id": 3, "name": "Following Name"}
                            ]}}}}}}
}

get_tweet_spec = {
    "description": "Твиты на кого подписан",
    "tags": ["get_tweets"],
    "parameters": [
        {
            "in": "header",
            "name": "Api-key",
            "type": "int",
            "required": True,
            "description": "Api-key of the user",
        }
    ],
    "responses": {
        200: {
            "description": "Показывает твиты на кого подписан подписан целевой юзер",
            "content": {
                "application/json": {
                    "example": {
                        "result": "true",
                        "tweets": {
                            "id": 1,
                            "content": "string",
                            "attachments": "url to static images",
                            "author": {
                                "id": "int",
                                "name": "string",
                            },
                            "likes": [
                                {"user_id": "int", "name": "string"}
                            ],
                        }}}}}}}

post_tweet_spec = {
    "description": "Создает твит",
    "tags": ["post_tweet"],
    "parameters": [
        {
            "in": "header",
            "name": "Api-key",
            "type": "int",
            "required": True,
            "description": "Api-key of the user",
        }
    ],
    "responses": {
        201: {
            "description": "Создание твита",
            "content": {
                "application/json": {
                    "example": {
                        "result": "true",
                        "tweet_id": "int"
                    }}}}}}
delete_tweet_id_spec = {
    "description": "Удаляет твит",
    "tags": ["delete_tweet"],
    "parameters": [
        {
            "in": "header",
            "name": "Api-key",
            "type": "int",
            "required": True,
            "description": "Api-key of the user",
        },
        {
            "in": "path",
            "name": "id",
            "type": "int",
            "required": True,
            "description": "target id tweet",
        }
    ],
    "responses": {
        200: {
            "description": "Удаление твита",
            "content": {
                "application/json": {
                    "example": {
                        "result": "true"
                    }}}}}}

post_medias_spec = {
    "description": "Принимает картинку к твиту",
    "tags": ["post_medias"],
    "parameters": [
        {
            "in": "formData",
            "name": "file",
            "type": "file",
            "required": True,
            "description": "Передаваемая картинка",
        }
    ],
    "responses": {
        200: {
            "description": "Принимает картинку к твиту",
            "content": {
                "application/json": {
                    "example": {
                        "result": "true",
                        "media_id": "int"
                    }}}}}}

post_like_spec = {
    "description": "Ставит лайк твиту",
    "tags": ["post_like"],
    "parameters": [
        {
            "in": "header",
            "name": "Api-key",
            "type": "int",
            "required": True,
            "description": "Api-key of the user",
        },
        {
            "in": "path",
            "name": "id",
            "type": "int",
            "required": True,
            "description": "target id tweet",
        }
    ],
    "responses": {
        201: {
            "description": "Ставит лайк твиту",
            "content": {
                "application/json": {
                    "example": {
                        "result": "true"
                    }}}}}}

delete_like_spec = {
    "description": "Убирает лайк твиту",
    "tags": ["delete_like"],
    "parameters": [
        {
            "in": "header",
            "name": "Api-key",
            "type": "int",
            "required": True,
            "description": "Api-key of the user",
        },
        {
            "in": "path",
            "name": "id",
            "type": "int",
            "required": True,
            "description": "target id tweet",
        }
    ],
    "responses": {
        200: {
            "description": "Убирает лайк твиту",
            "content": {
                "application/json": {
                    "example": {
                        "result": "true"
                    }}}}}}

post_follow_spec = {
    "description": "Подписывается на пользователя",
    "tags": ["post_follow"],
    "parameters": [
        {
            "in": "header",
            "name": "Api-key",
            "type": "int",
            "required": True,
            "description": "Api-key of the user",
        },
        {
            "in": "path",
            "name": "id",
            "type": "int",
            "required": True,
            "description": "target id tweet",
        }
    ],
    "responses": {
        201: {
            "description": "Подписывается на пользователя",
            "content": {
                "application/json": {
                    "example": {
                        "result": "true"
                    }}}}}}

delete_follow_spec = {
    "description": "Убирает подписку на пользователя",
    "tags": ["delete_follow"],
    "parameters": [
        {
            "in": "header",
            "name": "Api-key",
            "type": "int",
            "required": True,
            "description": "Api-key of the user",
        },
        {
            "in": "path",
            "name": "id",
            "type": "int",
            "required": True,
            "description": "target id tweet",
        }
    ],
    "responses": {
        200: {
            "description": "Убирает подписку на пользователя",
            "content": {
                "application/json": {
                    "example": {
                        "result": "true"
                    }}}}}}
