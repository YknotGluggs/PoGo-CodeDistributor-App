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
from kivy.graphics.texture import Texture
import qrcode
import json

# Python 3.12.0
#https://store.pokemongo.com/offer-redemption?passcode=68TTGWN79E7XE
codes = []
theme = "default"
state = 0

class CircleButton(ButtonBehavior, Widget):

    def __init__(self, image_source="", **kwargs):
        super().__init__(**kwargs)

        self.size_hint = (None, None)
        self.size = (65, 65)
        # Add image
        with self.canvas.before:
            Color(0.5, 0.5, 0.5, 1)
            self.rectangle = Rectangle(pos=self.pos, size=self.size)
            
        self.image = Image(
            source=image_source,
            pos = (
                self.x + (self.width * 0.15),
                self.y + (self.height * 0.15)
            ),
            size_hint = (None,None),
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

        
        self.image.size = (self.size[0]*0.7, self.size[1]*0.7)
        self.image.pos = (
            self.x + (self.width * 0.15),
            self.y + (self.height * 0.15)
        )

class QRButton(ButtonBehavior, FloatLayout):
    def __init__(self, image_source="", **kwargs):
        super().__init__(**kwargs)

        self.size_hint = (None, None)
        self.size = (250, 250)

        with self.canvas.before:
            Color(0.5,0.5,0.5,1)
            self.rectangle = Rectangle(pos=self.pos, size=self.size)

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
        self.rectangle.pos = self.pos
        self.rectangle.size = self.size

        self.image.pos = (
            self.x + (self.width - self.image.width) / 2,
            self.y + (self.height - self.image.height) / 2
        )
    
    def set_image_scale(self, scale):
        self.image.size = (
            self.width * scale,
            self.height * scale
        )
        self.image.pos = (
            self.x + (self.width - self.image.width) / 2,
            self.y + (self.height - self.image.height) / 2
        )

class QRWidget(FloatLayout):

    def __init__(self, data=[], index=0,**kwargs):
        super().__init__(**kwargs)

        self.orientation = "vertical"
        self.spacing = 10
        self.index = index

        # QR image
        self.qr_image = QRButton()
        self.qr_image.size_hint = (None, None)
        self.qr_image.size = (380, 380) # MAKE THIS DYNAMIC TO WINDOW SIZE
        self.qr_image.pos_hint = {
            "center_x": 0.5,
            "center_y": 0.6
        }
        # Text label
        self.code_label = Label(
            text=data[0],
            size_hint=(1, 0.10),
            pos_hint={"x": 0, "y": 0},
            color=(1, 1, 1, 1),
            font_size=20
        )
        self.qr_image.bind(on_press=lambda instance: self.chage_status())

        next_button = CircleButton(image_source="Images/icon_right_arrow.png")
        next_button.pos_hint = {"right": 1, "y": 0}
        next_button.bind(on_press=self.next_qr)

        back_button = CircleButton(image_source="Images/icon_left_arrow.png")
        back_button.pos_hint = {"x": 0, "y": 0}
        back_button.bind(on_press=self.prev_qr)

        self.add_widget(self.qr_image)
        self.add_widget(self.code_label)
        self.add_widget(next_button)
        self.add_widget(back_button)

        self.update_qr(data)

    def next_qr(self, instance):
        self.index = (self.index + 1) % len(codes)
        self.update_qr(codes[self.index])
        

    def prev_qr(self, instance):
        self.index = (self.index - 1) % len(codes)
        self.update_qr(codes[self.index])

    def update_qr(self, data):
        # Update label text
        self.code_label.text = data[0]
        if data[1]:
            self.qr_image.set_image_scale(0.90)
        else:
            self.qr_image.set_image_scale(1.0)
        self.qr_image.pos_hint = {"center_x": 0.5, "center_y": 0.5}


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
        cropped_texture = texture.get_region(10,10,390,390)

        self.qr_image.image.texture = cropped_texture
    
    def chage_status(self, ):
        codes[self.index][1] = (codes[self.index][1] + 1) % 2
        self.update_qr(codes[self.index])

class 

class HomeMenu(FloatLayout):
    def __init__(self, image_source="", **kwargs):
        super().__init__(**kwargs)

        self.image = Image(
            source=image_source,
            size_hint=(1, 1),
            pos_hint={"x": 0, "y": 0},
            allow_stretch=True,
            keep_ratio=True
        )

        self.add_widget(self.image)

        self.qr_widget = QRWidget(codes[0], index=0)
        self.qr_widget.size_hint = (None, None)
        self.qr_widget.size = (300, 500)
        self.qr_widget.pos_hint = {
            "center_x": 0.5,
            "center_y": 0.5
        }

        self.add_widget(self.qr_widget)

class Menubutton(ButtonBehavior, FloatLayout):
    def __init__(self, image_source="", **kwargs):
        super().__init__(**kwargs)
        self.size_hint_x = 0.34
        self.size_hint_y = None
        self.height = 80
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

        if state == 0:
            self.add_widget(HomeMenu(image_source="Images/background.jpg"))
        elif state == 1:
            # Add settings widget here
            pass
        elif state == 2:
            pass
        
        home_button = Menubutton(image_source='Images/icon_home.png')
        home_button.pos_hint = {"x": 0.33, "y": 0}
        home_button.bind(on_press=self.home)

        codes_button = Menubutton(image_source="Images/icon_codes.png")
        codes_button.pos_hint = {"x": 0, "y": 0}
        codes_button.bind(on_press=self.codes)

        upload_button = Menubutton(image_source="Images/icon_upload.png")
        upload_button.pos_hint = {"x": 0.66, "y": 0}
        upload_button.bind(on_press=self.upload)


        self.add_widget(home_button)
        self.add_widget(codes_button) 
        self.add_widget(upload_button)


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