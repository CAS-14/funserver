from server import Server

app = Server()

posts = {
    0: "hello world",
    1: "i like dogs",
    2: "i like cats"
}

@app.route("/")
@app.route("/home")
def home():
    return app.render("home.html")

@app.route("/post/<pid>")
def post(pid):
    if pid in posts:
        return app.render("post.html", content=posts[pid])
    else:
        return app.render("notfound.html", pid=pid)