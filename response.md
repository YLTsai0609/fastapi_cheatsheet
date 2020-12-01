# Default

``` Python
from fastapi import FastAPI

app = FastAPI()

@app.get("/")
async def root():
    return {'msg' : 'hello world'}
```

By default, FastAPI will return `JSONResponse`

# Custom

you can return `Response` object directly, bit the data won't be automatically converted, and the documentation won't be automatically generated.

| type of response | object in fastapi  | note |
|------------------|--------------------|------|
| json   | ORJSONResponse  |      if you want faster|
|html|HTTPResponse||
|custom|override the Response class|if no one fit your need|
|plain text|PlainTextResponse|
|redirection|RedirectResponse|
|streamming|StreammingResponse|
|file-like|StreammingResponse|
|file-like|FileResponse|
