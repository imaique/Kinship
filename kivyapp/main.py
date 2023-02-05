from kivy.app import App
from kivy.lang import Builder
from kivy.utils import platform
from kivy.uix.screenmanager import ScreenManager, Screen, NoTransition
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.togglebutton import ToggleButton
from kivy.properties import StringProperty, BooleanProperty, NumericProperty
import time
# from kivy.uix.image import Image
import os
from kivy.uix.scatter import Scatter
from kivy.properties import StringProperty
import requests
import base64

if platform == 'android':
    import android
    from android.permissions import Permission, request_permissions
    def callback(permission, results):
        if all([res for res in results]):
            print("Got all permissions")
        else:
            print("Did not get all permissions")
    request_permissions([Permission.CAMERA], callback)
# , Permission.WRITE_EXTERNAL_STORAGE,Permission.READ_EXTERNAL_STORAGE


link = 'https://kinship-api.herokuapp.com/userinfo'
myobj = {'somekey': 'somevalue'}
x = requests.post(url, json = myobj)
print(x.text)

PARAMS = {'address':'Name'}
r = requests.get(url = link, params = PARAMS)
data = r.json()
print(data)


class Picture(Scatter):
    source = StringProperty(None)

# picture a la fin
directory = '/home/max/home/POLYHACKS/V1/'



class MenuScreen(Screen):
    def request(self):
        resp = requests.post(link, data={'website': 'image'})
        print(resp.json())
        print(requests.post(link).json())

class Eventlist(Screen):

    def create(self, event):
        self.events = Button(text=event,on_press=self.test2,size_hint=(.7,None),height="50dp")
        self.logo = Button(text='infos',on_press=self.test,size_hint=(.3,None),height="50dp")
        # self.logo.bind(on_press = self.test)
        self.ids.stack_id.add_widget(self.events)
        self.ids.stack_id.add_widget(self.logo)


    def test(self,self2):
        self.manager.current = 'Myinfos'

    def test2(self, self2):
        self.manager.current = 'Maincamscreen'


class Myinfos(Screen):

    def create(self, Link):
        self.Link = Label(text=Link,on_press=self.test2,size_hint=(.7,None),height="50dp")
        self.logo = Label(text='logo',on_press=self.test,size_hint=(.3,None),height="50dp")
        # self.logo.bind(on_press = self.test)
        self.ids.stack_idi.add_widget(self.Link)
        self.ids.stack_idi.add_widget(self.logo)

        with open(str(directory+'profile.jpg'), "rb") as image_file:
            encoded_string = base64.b64encode(image_file.read())
        
        myobj = {'Photo': encoded_string, 'Linkedin': str(Link), 'Nom':'Michael'}
        requests.post(link, json = myobj)


    def test(self,self2):
        print('fk')

    def test2(self, self2):
        self.manager.current = 'Maincamscreen'



class Camscreen(Screen):
    def take_pic(self):
        try:                           
            camera = self.ids['camera']     
            camera.texture.save(str(directory+'profile.jpg'))
        except:
            print('pics not wroked')
        pass
        
    


class Maincamscreen(Screen):
    
    def take_pic(self):
        global data
        try:
            if not os.path.exists(str(directory+'1.jpg')):                            
                camera = self.ids['camera']     
                camera.texture.save(str(directory+'1.jpg'))
            else:
                print('Picture already exists')
        except:
            print('pics not wroked')

        with open(str(directory+'1.jpg'), "rb") as image_file:
            encoded_string = base64.b64encode(image_file.read())
        
        myobj = {'Photo': encoded_string}
        data = requests.post(link, json = myobj)
        pass


    def display_pic(self):
        time.sleep(1000)
        try:                            
            picture = Picture(source=str(directory+'1.jpg'))
            self.ids.anchor.add_widget(picture)
        except:
            print('pics not wroked')
        


class DisplayInfos(Screen):
    name = StringProperty(None)
    # name = from api
    def create(self, link):
        # on_press= from api
        self.link = Label(text=link,on_press=self.test2,size_hint=(.7,None),height="50dp")
        self.ids.stack_idis.add_widget(self.link)


class TheLabApp(App):
    def build(self):
        #Screens manager
        my_screenmanager = ScreenManager()
        screen1 = MenuScreen(name='menu')
        screen2 = Camscreen(name='Camscreen')
        screen3 = Eventlist(name='Eventlist')
        screen4 = Maincamscreen(name='Maincamscreen')
        screen5 = Myinfos(name='Myinfos')
        screen6 = DisplayInfos(name='DisplayInfos')

        my_screenmanager.add_widget(screen1)
        my_screenmanager.add_widget(screen2)
        my_screenmanager.add_widget(screen3)
        my_screenmanager.add_widget(screen4)
        my_screenmanager.add_widget(screen5)
        my_screenmanager.add_widget(screen6)


        return my_screenmanager



if __name__ == '__main__':
    TheLabApp().run()