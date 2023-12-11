import setuptools 
  
with open("README.md", "r") as fh: 
    description = fh.read() 
  
setuptools.setup( 
    name="qkogpt", 
    version="0.0.1", 
    author="EuiYul Song", 
    author_email="thddmlduf@gmail.com", 
    packages=["qkogpt"], 
    description="Quantized KoGPT", 
    long_description=description, 
    long_description_content_type="text/markdown", 
    license='MIT', 
    python_requires='>=3.10', 
    install_requires=[] 
) 
