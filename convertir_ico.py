from PIL import Image

# Convertir PNG a ICO
img = Image.open('static/img/OrganizeIt.png')
img.save('static/img/OrganizeIt.ico', format='ICO', sizes=[(256, 256)])
print("Icono convertido exitosamente a OrganizeIt.ico")