
from modules import RENDER
import web
from components import model

## For login test
class Login:
    def GET(self):
        login_form = self.login_form()
        register_form = self.registration_form()
        return RENDER.login(login_form, register_form)

    def create_login_form():
        ## Creates a 'Login' form that will appear on the webpage
        
        username_textbox = web.form.Textbox('username',
                                               web.form.notnull,
                                               description="Username")
        
        password_textbox = web.form.Password('password',
                                               web.form.notnull,
                                               description="Password")

        login_button = web.form.Button('Login',
                                        class_="btn btn-primary")

        form = web.form.Form(username_textbox,
                             password_textbox,
                             login_button)
        return form

    def create_registration_form():
        ## Creates a 'Register' form that will appear on the webpage
        
        username_textbox = web.form.Textbox('username',
                                               web.form.notnull,
                                               description="Username")
        
        password_textbox = web.form.Password('password',
                                               web.form.notnull,
                                               description="Password")

        register_button = web.form.Button('Register',
                                        class_="btn btn-info")

        form = web.form.Form(username_textbox,
                             password_textbox,
                             register_button)
        return form

    login_form = create_login_form()
    registration_form = create_registration_form()
    