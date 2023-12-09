import setuptools

with open("requirements.txt", "r") as f:
    requirements = f.read().splitlines()
setuptools.setup(
    name='AndN',
    version='0.4.7',
    url='https://github.com/grayrail000/AndroidQQ',
    packages=setuptools.find_packages(),
    license='',
    author='1a',
    author_email='',
    description='',
    install_requires=[
        'AndroidTools',
        'protobuf==4.23.4',
        'cryptography',
        'bs4',
        'urllib3==1.26.16'

    ]

)
