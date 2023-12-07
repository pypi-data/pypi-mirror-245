from setuptools import setup, find_packages

setup(
    name='shimpiproductions',
    version='0.2',
    packages=find_packages(),  # Include all packages in the directory
    install_requires=[
        'pandas',
        'scikit-learn',
        'numpy',
        'matplotlib',
        'apyori'
    ],
    entry_points={
        'console_scripts': [
            'main_script = shimpiproductions.main:main'
        ]
    },
    # Additional metadata
    author='SHIMPI PRODUCTIONS',
    author_email='sarveshshimpi18@gmail.com',
    description=open('README.txt').read(),
    long_description=open('README.txt').read(),
    long_description_content_type='text/markdown',
    url='https://upload.pypi.org/legacy/',
    password="pypi-AgEIcHlwaS5vcmcCJDAwNTRjNWJjLWFjMDctNDc5Ny04ZjZkLWFmYzQzNmUxNmMwOAACKlszLCI2Njg0NzZhMC1jMGM1LTQzZjQtOTBjYS03NzY1ZWMwNTI0N2MiXQAABiA6rLZe2t8h7peu78BS2tkTlghIM2Vp9mNno3PGvdJnVg",
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
)
