from kivymd.app import MDApp
from kivy.uix.screenmanager import ScreenManager, Screen
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.label import MDLabel
from kivymd.uix.textfield import MDTextField
from kivymd.uix.button import MDRaisedButton, MDFlatButton
from kivymd.uix.dialog import MDDialog

class SkincareApp(MDApp):
    def build(self):
        self.theme_cls.primary_palette = "Purple"
        self.conn = sqlite3.connect('skincare_app.db')  # SQLite database connection
        self.create_table()
        self.user_id = None
        self.sm = ScreenManager()

        # Create screens
        self.sm.add_widget(LoginScreen(name='login'))
        self.sm.add_widget(HomeScreen(name='home'))
        self.sm.add_widget(ProfileScreen(name='profile'))

        return self.sm

    def create_table(self):
        # Create users table if it doesn't exist
        with self.conn:
            self.conn.execute('''
                CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    username TEXT UNIQUE NOT NULL,
                    password TEXT NOT NULL
                )
            ''')

    def on_stop(self):
        # Close the database connection when the app is closed
        self.conn.close()


class LoginScreen(Screen):
    def __init__(self, **kwargs):
        super(LoginScreen, self).__init__(**kwargs)

        layout = MDBoxLayout(orientation='vertical', padding=10, spacing=10)
        self.username_input = MDTextField(hint_text='Username')
        self.password_input = MDTextField(hint_text='Password', password=True)
        login_button = MDRaisedButton(text='Login', on_release=self.login)
        create_user_button = MDRaisedButton(text='Create User', on_release=self.create_user)
        layout.add_widget(MDLabel(text='Login'))
        layout.add_widget(self.username_input)
        layout.add_widget(self.password_input)
        layout.add_widget(login_button)
        layout.add_widget(create_user_button)

        self.add_widget(layout)

    def login(self, instance):
        # Implement authentication logic here
        # Set user_id if login is successful
        username = self.username_input.text
        password = self.password_input.text

        with SkincareApp.get_running_app().conn:
            cursor = SkincareApp.get_running_app().conn.execute('SELECT id FROM users WHERE username=? AND password=?',
                                                                (username, password))
            user_id = cursor.fetchone()

        if user_id:
            SkincareApp.get_running_app().user_id = user_id[0]
            SkincareApp.get_running_app().sm.current = 'home'
        else:
            self.show_dialog('Error', 'Invalid username or password.')

    def create_user(self, instance):
        username = self.username_input.text
        password = self.password_input.text

        # Validate username and password
        if not username or not password:
            self.show_dialog('Error', 'Please enter both username and password.')
            return

        with SkincareApp.get_running_app().conn:
            # Check for duplicate username
            cursor = SkincareApp.get_running_app().conn.execute('SELECT id FROM users WHERE username=?', (username,))
            existing_user = cursor.fetchone()
            if existing_user:
                self.show_dialog('Error', 'Username already exists. Please choose a different one.')
                return

            # Store the new user in the database
            SkincareApp.get_running_app().conn.execute('INSERT INTO users (username, password) VALUES (?, ?)',
                                                       (username, password))

        # Inform the user that registration was successful
        self.show_dialog('Success', 'User registration successful. You can now log in.')

    def show_dialog(self, title, text):
        dialog = MDDialog(
            title=title,
            text=text,
            size_hint=(0.8, 0.4),
            buttons=[MDFlatButton(text="OK", on_release=lambda x: dialog.dismiss())],
        )
        dialog.open()


class HomeScreen(Screen):
    def __init__(self, **kwargs):
        super(HomeScreen, self).__init__(**kwargs)
        layout = MDBoxLayout(orientation='vertical', padding=10, spacing=10)
        layout.add_widget(MDLabel(text='Home Screen'))
        self.add_widget(layout)


class ProfileScreen(Screen):
    def __init__(self, **kwargs):
        super(ProfileScreen, self).__init__(**kwargs)
        layout = MDBoxLayout(orientation='vertical', padding=10, spacing=10)
        layout.add_widget(MDLabel(text='Profile Screen'))
        self.add_widget(layout)


if __name__ == '__main__':
    SkincareApp().run()
