import setuptools
setuptools.setup(
 name='Ceasar_encryptage',
 version='1.0.1',
 author="Cyberwolf",
 author_email="ralphsaintil0@gmail.com",
 description="c'est un algoritme de cryptage classique",
 packages=setuptools.find_packages(),
 install_requires=[
     'cryptography'
    ],
 classifiers=[
 "Programming Language :: Python :: 3",
 "License :: OSI Approved :: MIT License",
 "Operating System :: OS Independent",
 ],
)