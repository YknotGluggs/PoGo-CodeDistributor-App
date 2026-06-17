from kivy.config import Config
Config.set('graphics', 'width', '324')
Config.set('graphics', 'height', '723')
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.image import Image
from kivy.graphics import Color, Ellipse, Rectangle
from kivy.storage.jsonstore import JsonStore
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.clock import Clock
from kivy.graphics.texture import Texture
import qrcode
import json

# Python 3.12.0
#https://store.pokemongo.com/offer-redemption?passcode=68TTGWN79E7XE
codes = []
theme = "default"
state = 0

class BoxButton(ButtonBehavior, FloatLayout):

    def __init__(self, image_source="", **kwargs):
        super().__init__(**kwargs)

        self.size_hint = (0.12, 0.06)
        # Add image
        with self.canvas.before:
            Color(0.5, 0.5, 0.5, 1)
            self.rectangle = Rectangle(pos=self.pos, size=self.size)
            
        self.image = Image(
            source=image_source,
            size_hint = (None, None),
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

        
        self.image.size = (self.width*0.7, self.height * 0.7)
        self.image.pos = (
            self.x + (self.width - self.image.width) / 2,
            self.y + (self.height - self.image.height) / 2
        )

class QRButton(ButtonBehavior, FloatLayout):
    def __init__(self, image_source="", **kwargs):
        super().__init__(**kwargs)

        self.size_hint = (None,None)
        #self.size = (250, 250)

        self.image = Image(
            source=image_source,
            size_hint=(None, None),
            size=self.size,
            allow_stretch=True,
            keep_ratio=True
        )

        self.add_widget(self.image)

        self.bind(pos=self.update_graphics,
                  size=self.update_graphics)

        self.update_graphics()

    def update_graphics(self, *args):
        self.image.size = self.size
        self.image.pos = (
            self.x + (self.width - self.image.width) / 2,
            self.y + (self.height - self.image.height) / 2
        )

        

class CodesMenu(FloatLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.size_hint = (1,1)
        self.text = ""

        def on_focus(instance, value):
            if value:
                print("Focused")
                instance._keyboard = instance._ensure_keyboard()
        
        def on_text(instance, value):
            print('The widget', instance, 'have:', value)
            self.text = value
            
        self.textinput = TextInput(focus=True, size_hint=(0.9, 0.5), padding=[10, 10, 10, 10], font_size=24)
        self.textinput.pos_hint = {"x":0.05, "y":0.25}
        self.textinput.bind(text=on_text)
        self.textinput.bind(focus=on_focus)

        self.add_widget(self.textinput)

        

        

class HomeMenu(FloatLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.size_hint = (1,1)
        self.orientation = "vertical"
        self.spacing = 10
        self.index = 0
        self.data = codes[self.index]

        # QR image
        self.qr_image = QRButton()
        self.qr_image.size_hint = (0.8, 0.9)
        # Text label
        
        self.qr_image.bind(on_press=lambda instance: self.chage_status())

        self.next_button = BoxButton(image_source="Images/icon_right_arrow.png")
        self.next_button.size_hint = (0.12, 0.06)
        self.next_button.pos_hint = {"right": 0.9, "y": 0.25}
        self.next_button.bind(on_press=self.next_qr)

        self.back_button = BoxButton(image_source="Images/icon_left_arrow.png")
        self.back_button.size_hint = (0.12, 0.06)
        self.back_button.pos_hint = {"x": 0.1, "y": 0.25}
        self.back_button.bind(on_press=self.prev_qr)

        self.code_label = Label(
            text=self.data[0],
            size_hint=(1, 0.10),
            color=(0, 0, 0, 1),
            font_size=24
        )

        self.code_label.center_y = self.next_button.center_y
        self.code_label.center_x = (self.next_button.center_x + self.back_button.center_x) / 2

        with self.code_label.canvas.before:
            Color(1, 1, 1, 1)  # white
            self.code_label_bg = Rectangle(
                pos=(self.back_button.right, self.back_button.y),
                size=(self.next_button.x - self.back_button.right, self.back_button.height)
            )

        self.code_label.bind(
            pos=self.update_label_bg,
            size=self.update_label_bg
        )
        
        self.add_widget(self.qr_image)
        self.add_widget(self.code_label)
        self.add_widget(self.next_button)
        self.add_widget(self.back_button)

        
        self.bind(pos=self.update_graphics,
                  size=self.update_graphics)
        Clock.schedule_once(lambda dt: self.update_qr(codes[self.index]), 0)

    def next_qr(self, instance):
        self.index = (self.index + 1) % len(codes)
        self.update_qr(codes[self.index])
        

    def prev_qr(self, instance):
        self.index = (self.index - 1) % len(codes)
        self.update_qr(codes[self.index])

    def update_graphics(self, *args):
        self.qr_image.size_hint = (0.8, 0.8)
        self.qr_image.pos_hint = {"center_x": 0.5, "center_y": 0.5}

        self.back_button.pos_hint = {"x": 0.10, "y": 0.25}
        self.next_button.pos_hint = {"right": 0.90, "y": 0.25}

        self.code_label.center_y = self.next_button.center_y
        self.code_label.center_x = self.width / 2

    def update_qr(self, data):
        # Update label text
        self.code_label.text = data[0]
        self.update_graphics()
        


        # Generate QR
        qr = qrcode.make(f"https://store.pokemongo.com/offer-redemption?passcode={data[0]}")
        qr = qr.convert("RGBA")

        texture = Texture.create(
            size=   qr.size,
            colorfmt="rgba"
        )

        texture.blit_buffer(
            qr.tobytes(),
            colorfmt="rgba",
            bufferfmt="ubyte"
        )

        texture.flip_vertical()

        self.qr_image.image.texture = texture
    
    def chage_status(self, ):
        codes[self.index][1] = (codes[self.index][1] + 1) % 2
        self.update_qr(codes[self.index])
    
    def update_label_bg(self, *args):
        self.code_label_bg.pos = (self.back_button.right, self.back_button.y)
        self.code_label_bg.size = (self.next_button.x - self.back_button.right, self.back_button.height)

class Menubutton(ButtonBehavior, FloatLayout):
    def __init__(self, image_source="", **kwargs):
        super().__init__(**kwargs)
        self.color = (1,1,1,1)
        self.size_hint_x = 0.34
        self.size_hint_y = 0.08
        self.rectangle = Rectangle(pos=self.pos, size=self.size)
        '''
        with self.canvas.before:
            Color(0.5, 0.5, 0.5, 1)
            
        '''
        # Add image
        self.image = Image(
            source=image_source,
            size_hint=(1, 1),
            pos_hint={"x": 0, "y": 0},
            allow_stretch=True,
            keep_ratio=True
        )
        self.image.color = self.color

        self.add_widget(self.image)

        self.bind(pos=self.update_graphics,
                  size=self.update_graphics)

        self.update_graphics()

    def update_graphics(self, *args):
        self.rectangle.pos = self.pos
        self.rectangle.size = self.size
    
    


class overall_layout(FloatLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = "vertical"
        self.spacing = 10
        self.image = Image(
            source="Images/background.jpg",
            size_hint=(1, 1),
            pos_hint={"x": 0, "y": 0},
            allow_stretch=True,
            keep_ratio=True
        )
        self.add_widget(self.image)
        
        home_button = Menubutton(image_source='Images/icon_home.png')
        home_button.pos_hint = {"x": 0.33, "y": 0}
        home_button.bind(on_press=self.home)

        codes_button = Menubutton(image_source="Images/icon_codes.png")
        codes_button.pos_hint = {"x": 0, "y": 0}
        codes_button.bind(on_press=self.codes)

        upload_button = Menubutton(image_source="Images/icon_upload.png")
        upload_button.pos_hint = {"x": 0.66, "y": 0}
        upload_button.bind(on_press=self.upload)

        if state == 0:
            self.add_widget(HomeMenu())
            home_button.image.color = (0.5,0.5,0.5,1)
        elif state == 1:
            self.add_widget(CodesMenu())
            codes_button.image.color = (0.5,0.5,0.5,1)
        elif state == 2:
            upload_button.image.color = (0.5,0.5,0.5,1)


        self.add_widget(home_button)
        self.add_widget(codes_button) 
        self.add_widget(upload_button)

        self.bind(pos=self.update_graphics,
                  size=self.update_graphics)

        self.update_graphics()
    
    def update_graphics(self, *args):
        self.image.size_hint = (1,1)


    def home(self, instance):
        global state
        if state == 0:
            return
        state = 0
        print('home')
        self.clear_widgets()
        self.__init__()

    def codes(self, instance):
        global state
        if state == 1:
            return
        state = 1
        print('codes')
        self.clear_widgets()
        self.__init__()
    
    def upload(self, instance):
        global state
        if state == 2:
            return
        state = 2
        print('upload')
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