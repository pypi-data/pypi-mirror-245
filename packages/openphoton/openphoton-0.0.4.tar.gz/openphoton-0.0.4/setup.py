from setuptools import setup, find_packages

VERSION = '0.0.4'
DESCRIPTION = 'A scalar diffraction simulation package'
LONG_DESCRIPTION = 'A basic optics package for scalar diffraction simulation.'

# Setting up
setup(
    name="openphoton",
    version=VERSION,
    author="Gilbert M. Oca",
    author_email="<boyfriendnibluefairy@gmail.com>",
    license="MIT",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=LONG_DESCRIPTION,
    packages=find_packages(),
    install_requires=['numpy', 'scipy', 'Pillow'],
    keywords=['python', 'optics', 'diffraction', 'simulation', 'lens', 'SLM', 'light', 'wave', 'propagation'],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)