from fastapi import FastAPI, HTTPException
from sqlite3 import connect

from secrets import token_hex

from fastapi.responses import (
    JSONResponse,
    RedirectResponse
)

app = FastAPI()

database = connect('database.db')
cursor = database.cursor()

cursor.execute("CREATE TABLE IF NOT EXISTS links (code TEXT, link TEXT)")
database.commit()


def has_permission(token): return True if token else False


@app.get('/go/{code}')
async def go_to_link(code: str):

    cursor = database.cursor()

    cursor.execute("SELECT link FROM links WHERE code=?", (code, ))

    for link, in cursor:

        return RedirectResponse(link, 308)

    return HTTPException(404)


@app.get('/links')
async def get_links(token: str):

    if not has_permission(token):
        return HTTPException(403)

    cursor = database.cursor()

    links = []

    cursor.execute("SELECT * FROM links")

    for code, link in cursor:

        links.append({'code': code, 'link': link})

    return JSONResponse(links)


@app.put('/add')
async def put_link(token: str, link: str):

    if not has_permission(token):
        return HTTPException(403)

    cursor = database.cursor()

    code = ""
    found = False

    while not found:

        code = token_hex(3).upper()

        cursor.execute("SELECT * FROM links WHERE code=?", (code, ))

        if not [v for v in cursor]:

            found = True

    cursor.execute("INSERT INTO links (code, link) VALUES (?, ?)", (code, link))

    database.commit()

    return JSONResponse({'code': code, 'link': link})


@app.post('/edit')
async def edit_link(token: str, code: str, new_link: str):

    if not has_permission(token):
        return HTTPException(403)

    cursor = database.cursor()

    cursor.execute("SELECT * FROM links WHERE code=?", (code, ))

    for code, old_link in cursor:

        cursor.execute("UPDATE links SET link=? WHERE code=?", (new_link, code))

        database.commit()

        return JSONResponse({'code': code, 'old_link': old_link, 'new_link': new_link})

    return HTTPException(404)


@app.delete('/delete')
async def delete_link(token: str, code: str):

    if not has_permission(token):
        return HTTPException(403)

    cursor = database.cursor()

    cursor.execute("SELECT * FROM links WHERE code=?", (code, ))

    for code, link in cursor:

        cursor.execute("DELETE FROM links WHERE code=?", (code, ))

        database.commit()

        return JSONResponse({'code': code, 'link': link})

    return HTTPException(404)
