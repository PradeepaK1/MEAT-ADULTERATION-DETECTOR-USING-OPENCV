from kivy.app import App



from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.lang.builder import Builder
from kivy.uix.boxlayout import BoxLayout
import time
import numpy as np
import os
import cv2
from PIL import Image
from glob import glob


from kivy.uix.camera import Camera

from kivy.uix.boxlayout import BoxLayout

from kivy.uix.button import Button

from matplotlib import pyplot as plt
class LoginPage(Screen):
    def verify_credentials(self):
        if self.ids["login"].text == "username" and self.ids["passw"].text == "password":
            self.manager.current = "user"

class UserPage(Screen):
    def capture(self):

        camera = self.ids['camera']
        timestr = time.strftime("%Y%m%d_%H%M%S")
        camera.export_to_png('desktop/beef1/test2.png'.format(timestr))
        print("Captured")


        for name in glob('desktop/beef1/*.png'):
            im = Image.open(name)
            name = str(name).rstrip(".png")
            im.save(name + '.tif', 'TIFF')
        img_mask = 'desktop/beef1/*.tif'
        img_names = glob(img_mask)

        for name in glob('desktop/beef1/*.jpg'):
            image_file = name
            img_org = Image.open(image_file)


            factor = 1
            width = int(800 * factor)
            height = int(495 * factor)

            img_anti = img_org.resize((width, height), Image.ANTIALIAS)
            name, ext = os.path.splitext(image_file)

            new_image_file = "%s%s%s" % (name, str(factor), ext)
            img_anti.save(new_image_file)
            print("resized file saved as %s" % new_image_file)
            import webbrowser
            webbrowser.open(new_image_file)
        for name in glob('desktop/beef1/*.jpg'):
            im = Image.open(name)
            name = str(name).rstrip(".jpg")
            im.save(name + '.png', 'PNG')
        img_mask = 'desktop/beef1/*.png'
        img_names = glob(img_mask)

        
        
        for fn in img_names:
            print('processing %s...' % fn,)
            imageNo1 = cv2.imread(fn, 0)

            cv2.ocl.setUseOpenCL(False)

            imageNo2 = cv2.imread('test2.tif',0) 

            imageNo1 = imageNo1[200:600, 200:1000] 
            orb = cv2.ORB_create()

            keypoint1, descriptor1 = orb.detectAndCompute(imageNo1,None)
            keypoint2, descriptor2 = orb.detectAndCompute(imageNo2,None)

            bfMatcher = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)

            matchResults = bfMatcher.match(descriptor1,descriptor2)

            matchResults = sorted(matchResults, key = lambda x:x.distance)
            resultImage = cv2.drawMatches(imageNo1,keypoint1,imageNo2,keypoint2,matchResults[:100], None, flags=2)
            plt.imshow(resultImage),plt.show()
            if (matchResults[200:250]):
                print ("90% unadulterated")
            elif (matchResults[170:199]):
                print ("80% unadulterated")
            elif (matchResults[140:169]):
                print ("70% unadulterated")
            elif (matchResults[106:139]):
                print ("60% Adulterated")
            elif (matchResults[85:105]):
                print ("Adulterated")
            elif (matchResults[1:84]):
                print ("Unknown object")
       

       

        

class ScreenManagement(ScreenManager):
    pass

kv_file = Builder.load_file('login.kv')

class LoginApp(App):
    def builder(self):
        return kv_file

if __name__ == '__main__':
    LoginApp().run()
