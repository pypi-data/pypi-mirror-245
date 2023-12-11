from setuptools import find_packages, setup

with open("bodronoyo/Readme.md","r") as f:
    deskripsi = f.read()

setup(
    name="Bodoronoyo",
    version = "0.0.1",
    description="package machine learning buatan indonesia",
    package_dir={"":"bodronoyo"},
    packages=find_packages(where='bodronoyo'),
    long_description=deskripsi,
    long_description_content_type='text/markdown',
    url = 'https://github.com/khalifardy/library_machine_learning',
    author = 'Miko',
    author_email= 'khalifardy.miqdarsah@gmail.com',
    license= 'GNU',
    classifiers=[
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3.12',
    ],
    install_requires = [
        'numpy >= 1.26.2',
        'seaborn >= 0.13.0',
        'matplotlib >= 3.8.2',
        'scikit-learn >= 1.3.2',
        'pandas >= 2.1.4'
    ],
    python_requires = ">=3.10"
)

