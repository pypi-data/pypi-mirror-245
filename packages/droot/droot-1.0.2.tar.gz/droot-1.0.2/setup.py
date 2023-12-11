from setuptools import setup,find_packages

with open("README.md", "r", encoding='utf-8') as fh:
    long_description = fh.read()
setup(
    name='droot',
    version='1.0.2',
    description='Description of your package',
    author='hanbuhuai',
    long_description=long_description,
    author_email='2578187302@qq.com',
    
    long_description_content_type="text/markdown",
    license="MIT",
    py_modules=['droot'],
    install_requires=[
        # List any dependencies your package requires
    ],
)

