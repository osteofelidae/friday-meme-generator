#Imports required modules
import random
import requests
import shutil
from bs4 import BeautifulSoup
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
import os

#Defines Firefox headers
headers = {
    'Access-Control-Allow-Origin': '*',
    'Access-Control-Allow-Methods': 'GET',
    'Access-Control-Allow-Headers': 'Content-Type',
    'Access-Control-Max-Age': '3600',
    'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:52.0) Gecko/20100101 Firefox/52.0'
    }

#Copy word list to array variable
wordfile = open("dict.txt");
wordlist = wordfile.readlines()
wordfile.close()

#Choose a random word
word = random.choice(wordlist)
print(word)

#Load and parse google search page for selected word
searchaddress = "https://www.google.com/search?q=" + word + "&sxsrf=ALiCzsYSJEQIhm1h-KDmBrsoXkUy7Dt-gg:1663985899880&source=lnms&tbm=isch&sa=X&ved=2ahUKEwiKu-TDrqz6AhX3IkQIHVAOARsQ_AUoAnoECAIQBA&biw=1879&bih=1051&dpr=1"
req = requests.get(searchaddress, headers)
soup = BeautifulSoup(req.content, 'html.parser')
imgaddress = str(soup.find_all("img")[2])

#Get source url for 2nd image result (the first one is bad)
imgurl = imgaddress[32:len(imgaddress)-3]
print(imgaddress)

#Downloads raw data of image from url
r = requests.get(imgurl, stream = True)
r.raw.decode_content = True
with open("imgfileraw",'wb') as f:
    shutil.copyfileobj(r.raw, f)
    
#Retrieve image type from headers
img = Image.open("imgfileraw")
imgformat = img.format.lower()
img.close()

#Remove image file if existing
if os.path.exists("imgfile."+imgformat):
  os.remove("imgfile."+imgformat)

#Change image extension to correct image type
os.rename("imgfileraw","imgfile."+imgformat)

#Resize image
img = Image.open("imgfile."+imgformat)
width, height = img.size
newsize = (width*5, height*5)
img = img.resize(newsize)
imgeditor = ImageDraw.Draw(img)

#Overlay text
myfont = ImageFont.truetype('arial.ttf', 60)
imgeditor.text((0, 0), word + " friday", font = myfont, fill=(255, 0, 0))
img.save("imgfile."+imgformat)

#Display image
img.show()