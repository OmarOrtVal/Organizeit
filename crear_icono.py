from PIL import Image
import os

# Abrir tu logo
img = Image.open('static/img/OrganizeIt.png')

# Redimensionar a tamaños comunes de iconos
img = img.resize((256, 256))

# Guardar como ICO
img.save('static/img/OrganizeIt.ico', format='ICO', sizes=[(256, 256)])

print("Icono creado: static/img/OrganizeIt.ico")