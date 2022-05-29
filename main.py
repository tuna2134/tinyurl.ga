from sanic import Sanic, response
from aiosqlite import connect
from lib import randomname


app = Sanic("sanic")


@app.before_server_start
async def setup_database(app, loop):
    global db
    db = await connect("main.db")
    await db.execute("CREATE TABLE IF NOT EXISTS urls (name TEXT, url TEXT)")
    await db.commit()

@app.get("/")
async def index(request):
    return response.text("Hello World!")

@app.get("/<name>")
async def short(request, name):
    cursor = await db.execute("SELECT url FROM urls WHERE name = ?", (name,))
    data = await cursor.fetchone()
    if data is None:
        return response.redirect("/")
    return response.redirect(data[0])

@app.post("/api")
async def create(request):
    data = request.json
    name = randomname(10)
    await db.execute("INSERT INTO urls VALUES(?, ?)", (name, data["url"]))
    await db.commit()
    return response.json({"url": name})


app.run("0.0.0.0", port=8000)