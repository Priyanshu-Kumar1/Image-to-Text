from inspect import FrameInfo
from kivy.core import image
from kivymd.uix.boxlayout import MDBoxLayout
from kivy.uix.image import Image
from kivymd.uix.button import MDRaisedButton
from kivy.graphics.texture import Texture
from kivymd.uix.label import MDLabel
from kivy.clock import Clock
from kivymd.app import MDApp
import pytesseract
import cv2


pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'


class MainApp(MDApp):

    def load_video(self, *args):
            ret, frame= self.capture.read()
            # frame initialize
            self.image_frame= frame
            buffer= cv2.flip(frame, 0).tostring()
            texture= Texture.create(size=(frame.shape[1], frame.shape[0]), colorfmt="bgr")
            texture.blit_buffer(buffer, colorfmt="bgr", bufferfmt="ubyte")
            self.image.texture= texture
        
    def take_picture(self, *args):
        image_name= "picture.png"
        img= cv2.cvtColor(self.image_frame, cv2.COLOR_BGR2GRAY)
        img= cv2.GaussianBlur(img, (3, 3), 0)
        img= cv2.threshold(img, 0, 255, cv2.THRESH_BINARY_INV+cv2.THRESH_OTSU)[1]
        text_data= pytesseract.image_to_string(img, lang="eng", config="--psm 6")
        self.label.text= text_data
        cv2.imshow("cv2 final image", img)
        

    def build(self):
        self.layout= MDBoxLayout(orientation= "vertical")
        self.image= Image()
        self.layout.add_widget(self.image)
        self.save_img_btn= MDRaisedButton(
            text= "Capture",
            pos_hint= {"center_x": .5, "center_y": .8}
        )
        self.label= MDLabel()
        self.layout.add_widget(self.label)
        self.save_img_btn.bind(on_release= self.take_picture)
        self.layout.add_widget(self.save_img_btn)
        self.capture= cv2.VideoCapture(0)
        Clock.schedule_interval(self.load_video, 1.0/30.0)

        return self.layout

       

        

MainApp().run()