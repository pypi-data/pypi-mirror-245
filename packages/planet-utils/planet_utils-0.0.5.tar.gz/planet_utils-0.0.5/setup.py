from setuptools import setup

setup(
    # Needed to silence warnings
    name='planet_utils',
    url='https://github.com/NASA-IMPACT/planet_utils',
    author='Ankur Kumar',
    author_email='ankurk017@gmail.com',
    # Needed to actually package something
    packages=['planet_utils'],
    #download_url='https://github.com/NASA-IMPACT/planet_utils/archive/refs/tags/0.0.3.tar.gz',
    keywords = ['planet', 'utils', 'smallsat', 'nasa', 'nasaimpact', 'planetscope'],
    # Needed for dependencies
    install_requires=open('requirements.txt').read().split('\n')[:-1],
    # *strongly* suggested for sharing
    version='0.0.5',
    license='MIT',
    description='The planetscope package is a tool specifically designed to read and plot data from the PlanetScope satellite imaging system.',
    # We will also need a readme eventually (there will be a warning)
    long_description=open('README.md').read(),
)
