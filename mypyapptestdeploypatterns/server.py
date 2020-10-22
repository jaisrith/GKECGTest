import tornado.ioloop
import tornado.web
import pymysql

class MainHandler(tornado.web.RequestHandler):
    def get(self):
        title = "DANGER"
        bgcolor = "darkred"
        self.render("template.html",title=title,bgcolor=bgcolor)
        print(self.request)

class ProbeHandler(tornado.web.RequestHandler):
    def get(self):
        try:
            db = pymysql.connect('localhost',"mypyappdbuser","password","mypyappdb")
            cursor = db.cursor()
            cursor.execute("SELECT VERSION()")
            result = cursor.fetchone()
            title = f"OK DB Version {result}" 
            bgcolor = "limegreen"
            self.set_status(200)
        except pymysql.Error as e:
            title = f"NOT OK {e}"
            bgcolor = "darkred"
            self.set_status(503)
        self.render("template.html",title=title,bgcolor=bgcolor)


def make_app():
    return tornado.web.Application([
        (r"/",MainHandler),
        (r"/isalive",ProbeHandler),
        (r"/isready",ProbeHandler),
           ])

if __name__ == "__main__":
    app = make_app()
    app.listen(8888)
    tornado.ioloop.IOLoop.current().start()