# install

fastapi - (starlette + pydantic)

uvicorn (ASGI server)

# getting start

1. starting code
2. 自動搞定了異常處理(detail none, error msg in json) - follow openapi schema
3. 自動搞定了型別處理(integrate with pydantic)
4. 可吃query string
5. HTTP protocol
6. root/docs 有互動式文件界面 - Swagger UI

   1. 有哪些API，吃什參數
   2. 互動介面讓其他開發者詢問該API，並查看回應，包含HTTP code，response body
   3. 每個API會會做哪些驗證，錯誤的時候會出什麼schema，像是Validation Error會出detail，loc，msg，type，也有HTTPValidationError

7. 也有另一種互動式文件界面，使用Redoc
8. asgi ? ASGI （Asynchronous Server Gateway Interface)是Django團隊提出的一種具有非同步功能的Python web 伺服器閘道器介面協議。能夠處理多種通用的協議型別，包括HTTP，HTTP2和WebSocket。

# upgrade example

``` Python

class Item(BaseModel):
    name: str
    price: float
    is_offer: Optional[bool] = None

@app.put("/items/{item_id}")
def update_item(item_id: int, item: Item):
    return {"item_name": item.name, "item_id": item_id}
```

1. 互動文件會自動更新，可疑接更新網頁，因為當初起uvicorn server時有下 `--reload`

# Recap

1. documentation : build-in(int, str)  and custom(like Item)
2. Editor support (Completion, Type checks)
3. data validation
4. conversion of input data (json, query, path, cookie, header, forms, files)
5. conversion of output data (datetime, uuid, dayabase model, ...)
6. automatic interactive API doc with Swagger UI / ReDoc

# More features and tutorial

1. Declaration of parameters from other different places like headers, cookies, form fileds and files
2. validation constraints like `max_length`,     `regax`
3. easy to use dependency injection system
4. security and authentication like OAuth2 with JWT tokens and HTTP Basic auth
5. declaring deeply nested JSON models(thanks to Pydantic)
6. WebSockets, GraphQL, CORS, Cookie Sessions(thanks to Starlette)

# Reference

[ASGI, what is it](https://www.mdeditor.tw/pl/p6YJ/zh-tw?fbclid=IwAR2oUEppPyRUgyhKBW5rNtkZAXiXHOazBSZzLqHTZaZ_s7t-J5LD5RYz1JM)
