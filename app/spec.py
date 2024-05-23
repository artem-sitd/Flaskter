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
    "description": "Стартовая страница",
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
