#la funcion find_packages nos va a ayudar a buscar y encontrar paquetes para que no tengamos
#que estar escribiendo todos los nombres en caso de que sean muchos paquetes
from setuptools import setup, find_packages

setup(
    name="Mensajes-DatoVirtual",
    version="3.0.0",
    description="Un paquete para saludar y despedir",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="Mauro M. Perez",
    author_email="mmp.datovirtual@gmail.com",
    url="https://www.datovirtual.net.ar",
    license_files=["LICENSE"],
    #packages=["mensajes", "mensajes.hola", "mensajes.adios"],
    packages=find_packages(),
    scripts=[],
    test_suite="tests",
    #de esta manera indicamos que nuestro paquete requiere instalar esta otra dependencia de paquete para que funcione
    #en caso de querer instalar una version en especifica poner "numpy==1.23.0"
    install_requires=[paquete.strip() for paquete in open("requirements.txt").readlines()],

    classifiers=[
        "Environment :: Console",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Topic :: Utilities",

    ]
)
#para instalar este paquete hay que ubiarse en la carpeta raiz del mismo donde se encuentra
#el archivo setup.py y el test.py con sus subcarpetas donde creamos los paquetes
#ejecutamos python setup.py sdist (para instalarlo)
#luego entramos en sdist y ejecutamos : pip install (nombre del modulo).tar.gz
#y listo ... luego cuando queramos actualizarlo por uno mejorado hacemos lo mismo pero
#pip install (nombre del paquete).tar.gz --upgrade

#luego para borrar el paquete se hace pip uninstall manesajes y confirmar con Y

#para crear el paquete y que sea publicado es necesario estos 2 paquetes
#build y twine instalarlos con pip install

#y luego de instalados python -m build
# python -m twine check dist/*