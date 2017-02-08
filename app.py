import os
import web

# seek templates in specified directory
render = web.template.render('templates/', base='')

# URL structure
urls = (
    '/', 'index',                                           # default index url
)

app = web.application(urls, globals())

# defining GET operation
class index:    
    def GET(self):
        web.header('Content-Type', 'text/html')
        return render.index()

def is_test():
    if 'WEBPY_ENV' in os.environ:
        return os.environ['WEBPY_ENV'] == 'test'

if (not is_test()) and __name__ == "__main__":
    app.run()
