from PIL import Image
from io import BytesIO


import requests
from bs4 import BeautifulSoup

class Iconfinder():
    
    parameter:str
    pricing:str
    links=[]
    count:int
    count=1

    def __init__(self,parameter):
        self.parameter=parameter
       

    def images(self):
     website=requests.get(f"https://www.iconfinder.com/search?q={self.parameter}").text
     parser=BeautifulSoup(website,'lxml')
     images=parser.find_all('div',class_='icon-preview-img d-flex align-items-center justify-content-center')
     

     for image in images:
        icon=image.find('img')['src']
        self.links.append(icon)
        print(f"Icon {self.count} \n",icon,"\n")
        self.count+=1
        

    def show_image(self,number:int):
     website=requests.get(f"https://www.iconfinder.com/search?q={self.parameter}").text
     parser=BeautifulSoup(website,'lxml')
     images=parser.find_all('div',class_='icon-preview-img d-flex align-items-center justify-content-center')
     

     for image in images:
        icon=image.find('img')['src']
        self.links.append(icon)
       

     firstimage=requests.get(self.links[number-1]) 
     im=Image.open(BytesIO(firstimage.content))  
     im.show()

    def get_links(self):
      website=requests.get(f"https://www.iconfinder.com/search?q={self.parameter}").text
      parser=BeautifulSoup(website,'lxml')
      links=parser.find_all('div',class_='icon-preview-bg')
      initial="https://www.iconfinder.com/"
      for link in links:
        route=link.find('a')['href']
        print(f"{initial}{route}")
    
    def save_image(self,path:str,number:int):
     website=requests.get(f"https://www.iconfinder.com/search?q={self.parameter}").text
     parser=BeautifulSoup(website,'lxml')
     images=parser.find_all('div',class_='icon-preview-img d-flex align-items-center justify-content-center')
     

     for image in images:
        icon=image.find('img')['src']
        self.links.append(icon)
       

     firstimage=requests.get(self.links[number-1]) 
     im=Image.open(BytesIO(firstimage.content))
     if im.mode == 'RGBA':
            im = im.convert('RGB')
     im.save(path)

class Iconfinder3D():
    parameter:str
    pricing:str
    links=[]
    count:int
    count=1

    def __init__(self,parameter):
       self.parameter=parameter
       

    def images(self):
     website=requests.get(f"https://www.iconfinder.com/search/3d-illustrations?q={self.parameter}").text
     parser=BeautifulSoup(website,'lxml')
     images=parser.find_all('div',class_='icon-preview-img d-flex align-items-center justify-content-center')
     

     for image in images:
        icon=image.find('img')['src']
        self.links.append(icon)
        print(f"Icon {self.count} \n",icon,"\n")
        self.count+=1
        

    def show_image(self,number:int):
     website=requests.get(f"https://www.iconfinder.com/search/3d-illustrations?q={self.parameter}").text
     parser=BeautifulSoup(website,'lxml')
     images=parser.find_all('div',class_='icon-preview-img d-flex align-items-center justify-content-center')
     

     for image in images:
        icon=image.find('img')['src']
        self.links.append(icon)
       

     firstimage=requests.get(self.links[number-1]) 
     im=Image.open(BytesIO(firstimage.content))  
     im.show()

    def get_links(self):
      website=requests.get(f"https://www.iconfinder.com/search/3d-illustrations?q={self.parameter}").text
      parser=BeautifulSoup(website,'lxml')
      links=parser.find_all('div',class_='icon-preview-bg')
      initial="https://www.iconfinder.com/"
      for link in links:
        route=link.find('a')['href']
        print(f"{initial}{route}")
    
    def save_image(self,path:str,number:int):
     website=requests.get(f"https://www.iconfinder.com/search/3d-illustrations?q={self.parameter}").text
     parser=BeautifulSoup(website,'lxml')
     images=parser.find_all('div',class_='icon-preview-img d-flex align-items-center justify-content-center')
     

     for image in images:
        icon=image.find('img')['src']
        self.links.append(icon)
       

     firstimage=requests.get(self.links[number-1]) 
     im=Image.open(BytesIO(firstimage.content))
     if im.mode == 'RGBA':
            im = im.convert('RGB')
     im.save(path)     

   

     
       






