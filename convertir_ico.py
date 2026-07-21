from PIL import Image

img = Image.open('static/img/OrganizeIt.png')
img.save('static/img/OrganizeIt.ico', format='ICO', sizes=[(256, 256)])
print("Icono convertido exitosamente a OrganizeIt.ico")