from setuptools import setup, find_packages

setup(
    name='forgecloud',  
    version='0.0.4', 
    author='Niclas Stoltenberg',  
    author_email='niclasjensen@example.com',  
    description='A package to connect and manage Forge apps with Google Cloud Functions',  
    long_description=open('README.md').read(),  
    long_description_content_type='text/markdown',  
    url='https://github.com/Ns85/forgecloud',  
    packages=find_packages(), 
    install_requires=[
        #'pandas==2.1.4', 
    ],
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',  
        'Intended Audience :: Developers',  
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: MIT License',  
        'Programming Language :: Python :: 3',  
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
    ],
    keywords='forge google-cloud-functions integration',  # Keywords for your package
    python_requires='>=3.7',  # Minimum version requirement of Python
)
