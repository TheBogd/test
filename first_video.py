
from functools import partial
from pytube import YouTube

from kivymd.uix.relativelayout import MDRelativeLayout

from kivymd.app import MDApp

from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.image import Image
from kivy.uix.button import Button
from kivy.uix.dropdown import DropDown
import re

from kivy.core.window import Window

Window.size=(500,500)


class MyApp(MDApp):
    
    def getLinkInfo(self,event, layout ):
    
        self.link=self.linkinput.text
        
        self.checklink=re.match("^https://www.youtube.com/.*",self.link)
        print(self.checklink)
        if self.checklink:
            
            self.errorLabel.text=""
            self.errorLabel.pos_hint={'center_x':0.5,'center_y':0.4}
            self.yt=YouTube(self.link)
            
            try:
                self.errorLabel.text=""
                self.errorLabel.pos_hint={'center_x':0.5,'center_y':0.4}
                self.titleLabel.text="Titlu: "+str(self.yt.title)
                textlenght=len("Titlu: \n"+str(self.yt.title))
                # Define the maximum width (in pixels) that the title label can occupy
                max_width = 1200  # Adjust this value according to your layout

                # Calculate the font size based on the text length and maximum width
                font_size = min(max_width / textlenght, 20)  
                self.titleLabel.pos_hint={'center_x':0.5,'center_y':0.40}
                self.titleLabel.font_size=font_size
                
                self.lenghtLabel.text="Lungime: "+str(self.yt.length)
                self.lenghtLabel.pos_hint={'center_x':0.5,'center_y':0.35}
                self.viewsLabel.text="Vizualizari: "+str(self.yt.views)
                self.viewsLabel.pos_hint={'center_x':0.5,'center_y':0.30}
                
                self.downloadButton.text="Download"
                self.downloadButton.pos_hint={'center_x':0.5,'center_y':0.20}
                self.downloadButton.size_hint=(.3,.1)
                
                self.video=self.yt.streams.filter(file_extension='mp4').order_by('resolution').desc()
                print(self.video)
                
                self.dropDown=DropDown()
                
                for video in self.video:
                    print(video)
                    btton=Button(text=video.resolution, size_hint_y=None, height=30)
                    btton.bind(on_release= lambda btton:self.dropDown.select(btton.text))
                    self.dropDown.add_widget(btton)
                
                self.main_button=Button(text='144p', size_hint=(None,None), pos=(350,65), height= 50)
                
                self.main_button.bind(on_release=self.dropDown.open)
                self.dropDown.bind(on_select=lambda instance, x:setattr(self.main_button,'text',x))
                
                layout.add_widget(self.main_button)
                
                
                print("Titlu: "+str(self.yt.title))
                print("Views: "+str(self.yt.views))
                print("Lungime: "+str(self.yt.length))
            except:
                self.errorLabel.text="Network Error"
                self.errorLabel.pos_hint={'center_x':0.5,'center_y':0.4}
                print("invalid link")
                return
        else:
            self.errorLabel.text="Invalid or Empty Link"
            self.errorLabel.pos_hint={'center_x':0.5,'center_y':0.4}
            print("invalid link")
            return
        
    def download(self,event,layout):
        self.ys=self.yt.streams.filter(file_extension='mp4').filter(res=self.main_button.text).first()
        print("Donloading")
        self.ys.download("D:/Songs")  
        print("Download Complete")  
    
    def build(self):
        layout = MDRelativeLayout(md_bg_color=[248/255,200/255,220/255])
        
        self.img=Image ( source='youtube.png', size_hint=(.5,.5),
                       pos_hint = {'center_x':0.5,'center_y':0.90})
        self.youtubelink=Label(text='Please enter  Youtube link u want 2 download', 
                               pos_hint={'center_x':0.5,'center_y':.75},
                               size_hint=(1,1), font_size=20, color=(1,0,0))
        
        self.linkinput = TextInput(text='', pos_hint={'cener_x':0.5, 'center_y':0.65},
                                   size_hint=(1,None),height=48,
                                   font_size=29, foreground_color=(0,.5,0),
                                   font_name="Comic")
        self.linkbutton=Button(text="Get Link", pos_hint={'center_x':0.5,'center_y':0.5},
                               size_hint=(.2,.1), font_name="Comic", font_size=24,
                               background_color=[0,1,0])
        
        self.titleLabel=Label(text="", pos_hint={'center_x':0.5,'center_y':20},
                              size_hint=(1,1), font_size=20)
        self.lenghtLabel=Label(text="", pos_hint={'center_x':0.5,'center_y':20},
                              size_hint=(1,1), font_size=20)
        self.viewsLabel=Label(text="", pos_hint={'center_x':0.5,'center_y':20},
                              size_hint=(1,1), font_size=20)
        
        self.downloadButton=Button(pos_hint={'center_x':0.5,'center_y':20},
                                   size_hint=(.2,.1),size=(75,75), font_name="Comic",
                                   bold=True, font_size=24, background_color=(0,1,0))
        
        self.downloadButton.bind(on_press=partial(self.download,layout))
        
        self.linkbutton.bind(on_press=partial(self.getLinkInfo,layout))
        self.errorLabel= Label(text='', pos_hint={'center_x':0.5,'center_y':20},
                               size_hint=(1,1), font_size=20, color=(1,0,0))
        
        layout.add_widget(self.img)
        layout.add_widget(self.youtubelink)
        layout.add_widget(self.linkinput)
        layout.add_widget(self.linkbutton)
        layout.add_widget(self.titleLabel)
        layout.add_widget(self.viewsLabel)
        layout.add_widget(self.lenghtLabel)
        layout.add_widget(self.downloadButton)
        layout.add_widget(self.errorLabel)
        
        
        return layout
    
if __name__=="__main__":
    MyApp().run()
