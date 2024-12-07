from setuptools import setup, find_packages

setup(
    name="MonsterBot",
    version="1.0",  
    packages=find_packages(),
    install_requires=[                
        'requests>=3.0',       
    ],
    author="MONSTER",
    author_email="oussamadev22@gmail.com",
    description="An Online chatbot librery",
    long_description_content_type='text/markdown',
    url="https://github.com/7lMONSTERl7/networkpwner.git",
    classifiers=[      
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
