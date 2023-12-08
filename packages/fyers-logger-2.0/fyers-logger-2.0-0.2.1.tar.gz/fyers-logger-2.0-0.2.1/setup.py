import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
     name='fyers-logger-2.0',  
     version='0.2.1',
     author="Fyers-Tech",
     author_email="support@fyers.in",
     description="Fyers Internal Logging Library",
     long_description=long_description,
     long_description_content_type="text/markdown",
     url="https://github.com/FyersDev/fyers-logger",
     py_modules=["fyers_logger"],
     python_requires='>=3.8',
     install_requires=[
                'python-json-logger==2.0.7',
          ],
     classifiers=[
         "Programming Language :: Python :: 3",
         "License :: OSI Approved :: MIT License",
         "Operating System :: OS Independent",
     ],
 )
