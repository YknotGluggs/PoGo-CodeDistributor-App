from kivy.app import App
from kivy.uix.widget import Widget
from kivy.properties import NumericProperty, ReferenceListProperty
from kivy.vector import Vector
from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.image import Image
from kivy.graphics import Color, Ellipse, Rectangle
from kivy.uix.boxlayout import BoxLayout
from kivy.storage.jsonstore import JsonStore
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.graphics.texture import Texture
import qrcode
import json

#https://store.pokemongo.com/offer-redemption?passcode=68TTGWN79E7XE
codes = []
theme = "default"
state = 0

class CircleButton(ButtonBehavior, Widget):

    def __init__(self, image_source="", **kwargs):
        super().__init__(**kwargs)

        self.size_hint = (None, None)
        self.size = (120, 120)

        # Draw circle
        with self.canvas.before:
            Color(1, 1, 1, 1)
            self.circle = Ellipse(pos=self.pos, size=self.size)

        # Add image
        self.image = Image(
            source=image_source,
            pos=self.pos,
            size=self.size,
            allow_stretch=True,
            keep_ratio=True
        )

        self.add_widget(self.image)

        self.bind(pos=self.update_graphics,
                  size=self.update_graphics)

        self.update_graphics()

    def update_graphics(self, *args):
        self.circle.pos = self.pos
        self.circle.size = self.size

        self.image.pos = self.pos
        self.image.size = self.size



class QRWidget(BoxLayout):

    def __init__(self, data=[], index=None,**kwargs):
        super().__init__(**kwargs)

        self.orientation = "vertical"
        self.spacing = 10

        self.size_hint = (None, None)
        self.size = (300, 350)
        self.index = index

        # QR image
        self.qr_image = Image(
            size_hint=(1, 0.85)
        )

        # Text label
        self.code_label = Label(
            text=data[0],
            size_hint=(1, 0.15),
            color=(1, 1, 1, 1),
            font_size=20
        )
        status = "Avaliable"
        if data[1] == 0:
            status = "Redeemed"

        self.status_Button = Button(
            text=status,
            size_hint=(1, 0.10),
            color=(1, 1, 1, 1),
            font_size=20
        )
        self.status_Button.bind(on_press=lambda instance: self.chage_status(self.index))


        self.add_widget(self.qr_image)
        self.add_widget(self.code_label)
        self.add_widget(self.status_Button)

        self.update_qr(data)

    def update_qr(self, data):

        # Update label text
        self.code_label.text = data[0]
        self.status_Button.text = "Avaliable" if data[1] == 0 else "Redeemed"

        # Generate QR
        qr = qrcode.make(f"https://store.pokemongo.com/offer-redemption?passcode={data[0]}")
        qr = qr.convert("RGBA")

        texture = Texture.create(
            size=qr.size,
            colorfmt="rgba"
        )

        texture.blit_buffer(
            qr.tobytes(),
            colorfmt="rgba",
            bufferfmt="ubyte"
        )

        texture.flip_vertical()

        self.qr_image.texture = texture
    
    def chage_status(self, index):
        codes[index][1] = (codes[index][1] + 1) % 2
        self.status_Button.text = "Avaliable" if codes[index][1] == 0 else "Redeemed"

class Code_layout(BoxLayout):
    velocity_x = NumericProperty(0)
    velocity_y = NumericProperty(0)
    velocity = ReferenceListProperty(velocity_x, velocity_y)

    def move(self):
        self.pos = Vector(*self.velocity) + self.pos
    

class Distribution(FloatLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.index = 0

        code_layout = Code_layout()
        self.qr_widget = QRWidget(codes[self.index], index=self.index)
        self.qr_widget.pos_hint = {
            "center_x": 0.5,
            "center_y": 0.5
        }


        next_button = CircleButton()
        next_button.pos_hint = {"right": 1, "center_y": 0.5}
        next_button.bind(on_press=self.next_qr)

        back_button = CircleButton()
        back_button.pos_hint = {"x": 0, "center_y": 0.5}
        back_button.bind(on_press=self.prev_qr)


        self.add_widget(self.qr_widget)
        self.add_widget(next_button)
        self.add_widget(back_button)

    def next_qr(self, instance):
        self.index = (self.index + 1) % len(codes)

        self.qr_widget.update_qr(codes[self.index])
        self.qr_widget.index = self.index

    def prev_qr(self, instance):
        self.index = (self.index - 1) % len(codes)

        self.qr_widget.update_qr(codes[self.index])
        self.qr_widget.index = self.index

class Menubutton(ButtonBehavior, Widget):
    def __init__(self, image_source="", **kwargs):
        super().__init__(**kwargs)
        self.size_hint = (None, None)
        self.size = (100, 50)
        
        with self.canvas.before:
            Color(1, 1, 1, 1)
            self.rectangle = Rectangle(pos=self.pos, size=self.size)

        # Add image
        self.image = Image(
            source=image_source,
            pos=self.pos,
            size=self.size,
            allow_stretch=True,
            keep_ratio=True
        )

        self.add_widget(self.image)

        self.bind(pos=self.update_graphics,
                  size=self.update_graphics)

        self.update_graphics()

    def update_graphics(self, *args):
        self.rectangle.pos = self.pos
        self.rectangle.size = self.size

        self.image.pos = self.pos
        self.image.size = self.size

    
    


class overall_layout(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = "vertical"
        self.spacing = 10

        if state == 0:
            self.add_widget(Distribution())
        elif state == 1:
            # Add settings widget here
            pass
        
        menu_button = Menubutton(image_source="")
        menu_button.pos_hint = {"right": 1, "y": 0}
        menu_button.bind(on_press=self.toggle_menu)
        self.add_widget(menu_button)

    def toggle_menu(self, instance):
        global state
        state = (state + 1) % 2
        self.clear_widgets()
        self.__init__()

        


class DistributorApp(App):
    def build(self):
        global codes, theme
        data = JsonStore('data.json')
        if data.exists('theme'):
            theme = data.get('theme')
            # Load theme settings if needed
        if data.exists('codes'):
            codes = data.get('codes')
            # Load codes if needed
        return overall_layout()

    def on_stop(self):
        data = {"theme": theme, "codes": codes}

        with open("data.json", "w") as file:
            json.dump(data, file)

        print("Data saved")

if __name__ == '__main__':
    DistributorApp().run()