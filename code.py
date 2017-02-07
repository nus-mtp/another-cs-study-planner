import os
import psycopg2
import web

# seek templates in specified directory
render = web.template.render('templates/', base='') # TODO: define a base layout
web.template.Template.globals['login_user'] = ''

# Creating database object
db = web.database(dbn='postgres', user='postgres', pw='12345', db='csmodify')

# URL structure
urls = (
    '/', 'index',                              # default index url
    '/login', 'login',
    '/register', 'register',
    "/home(.*)", 'home'
)

app = web.application(urls, globals())

# defining GET operation
class index:    
    def GET(self):
        web.header('Content-Type', 'text/html')
        return render.index()

class login:
    def GET(self):
        return render.login(1, None)
    
    def POST(self):
        user_input = web.input()                # gives access to variables of a form
        variables = dict(staffid=user_input.staffId)
        result = db.select('public.admin', where="staffid = $staffid", vars=variables)
        if len(result) == 1:
            for account in result:
                if account.isactivated == True:
                    print(user_input.staffId)
                    web.template.Template.globals['login_user'] = user_input.staffId
                    raise web.seeother('/home?id=' + user_input.staffId)
                else:
                    return render.login(-2, user_input.staffId)
        else:
            return render.login(-1, None)

class register:
    def GET(self):
        return render.register(0)

    def POST(self):
        user_input = web.input()
        if user_input.password == user_input.confirm_password:
            result = db.insert('public.admin', staffid=user_input.staffId, password=user_input.password)
            if result:
                return render.login(3, None)
            else:
                return render.register(-1)

class home:
    def GET(self, user):
        print(user)
        userid = web.input().id
        if web.template.Template.globals['login_user'] == userid:
            return render.home(userid)
        else:
            return web.notfound()

    def POST(self, user):
        web.template.Template.globals['login_user'] = ''
        raise web.seeother('/login')

def is_test():
    if 'WEBPY_ENV' in os.environ:
        return os.environ['WEBPY_ENV'] == 'test'

if (not is_test()) and __name__ == "__main__":
    app.run()
