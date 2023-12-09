from setuptools import setup, find_packages

setup(
    name='google_text_to_speech', 
    version='0.1.2',  
    package_dir={'': 'src'}, 
    packages=find_packages(where='src'), 
    description='A text-to-speech conversion tool using Google Translate API',  
    long_description=open('README.md').read(),  
    long_description_content_type='text/markdown',  
    author='Momcilo Krunic',
    author_email='momcilo.krunic@labsoft.ai',
    url='https://gitlab.com/labsoft-ai/google-translate-tts',
    license='MIT',
    install_requires=[
        "requests",
        "playsound"
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
)
