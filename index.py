from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button


class SkincareApp(App):
    def build(self):
        self.title = 'Skincare App'
        self.user_id = None

        # Create the main layout
        layout = BoxLayout(orientation='vertical', padding=10, spacing=10)

        # Create widgets
        label = Label(text='Welcome to Skincare App!')
        preferences_button = Button(text='Set Preferences', on_press=self.set_preferences)
        add_product_button = Button(text='Add Product', on_press=self.add_product)
        generate_routine_button = Button(text='Generate Skincare Routine', on_press=self.generate_routine)

        # Add widgets to the layout
        layout.add_widget(label)
        layout.add_widget(preferences_button)
        layout.add_widget(add_product_button)
        layout.add_widget(generate_routine_button)

        return layout

    def set_preferences(self, instance):
        popup_layout = BoxLayout(orientation='vertical', padding=10, spacing=10)
        skin_type_label = Label(text='Enter your skin type:')
        skin_type_input = TextInput(multiline=False)
        concerns_label = Label(text='Enter your skincare concerns (comma-separated):')
        concerns_input = TextInput(multiline=False)
        save_button = Button(text='Save', on_press=lambda instance: self.save_preferences(
            skin_type_input.text, concerns_input.text, popup.dismiss))
        popup_layout.add_widget(skin_type_label)
        popup_layout.add_widget(skin_type_input)
        popup_layout.add_widget(concerns_label)
        popup_layout.add_widget(concerns_input)
        popup_layout.add_widget(save_button)

        popup = self.create_popup('Set Preferences', popup_layout)
        popup.open()

    def add_product(self, instance):
        popup_layout = BoxLayout(orientation='vertical', padding=10, spacing=10)
        product_name_label = Label(text='Enter the name of the product:')
        product_name_input = TextInput(multiline=False)
        product_type_label = Label(text='Enter the type of the product:')
        product_type_input = TextInput(multiline=False)
        save_button = Button(text='Save', on_press=lambda instance: self.save_product(
            product_name_input.text, product_type_input.text, popup.dismiss))
        popup_layout.add_widget(product_name_label)
        popup_layout.add_widget(product_name_input)
        popup_layout.add_widget(product_type_label)
        popup_layout.add_widget(product_type_input)
        popup_layout.add_widget(save_button)

        popup = self.create_popup('Add Product', popup_layout)
        popup.open()

    def generate_routine(self, instance):
        if self.user_id is None:
            self.show_popup('Error', 'Please set preferences and add products first.')
        else:
            routine = self.skincare_app.generate_routine(user_id=self.user_id)
            routine_text = "\n".join([f"Step {step}: {product[0]} ({product[1]})" for step, product in enumerate(routine, start=1)])
            self.show_popup('Skincare Routine', routine_text)

    def save_preferences(self, skin_type, concerns, dismiss_function):
        # Save preferences to the database and update the UI
        self.user_id = 1  # Replace this with the actual user ID from the database
        self.skincare_app.set_preferences(user_id=self.user_id, skin_type=skin_type, concerns=concerns)
        dismiss_function()

    def save_product(self, product_name, product_type, dismiss_function):
        # Save product to the database and update the UI
        product_id = self.skincare_app.conn.execute(
            'INSERT INTO products (name, type, suitable_skin_types, concerns) VALUES (?, ?, ?, ?)',
            (product_name, product_type, 'All', 'All')
        ).lastrowid
        self.skincare_app.add_product(user_id=self.user_id, product_id=product_id)
        dismiss_function()

    def create_popup(self, title, content):
        from kivy.uix.popup import Popup
        popup = Popup(title=title, content=content, size_hint=(None, None), size=(400, 300))
        return popup

    def show_popup(self, title, message):
        popup_layout = BoxLayout(orientation='vertical', padding=10, spacing=10)
        message_label = Label(text=message)
        ok_button = Button(text='OK', on_press=lambda instance: popup.dismiss())
        popup_layout.add_widget(message_label)
        popup_layout.add_widget(ok_button)

        popup = self.create_popup(title, popup_layout)
        popup.open()


if __name__ == '__main__':
    SkincareApp().run()
