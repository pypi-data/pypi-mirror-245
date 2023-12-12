from setuptools import setup,find_packages
c=["Programming Language :: Python :: 3",
   "License :: OSI Approved :: MIT License",
   "Operating System :: OS Independent",]
d="This is fun Games Package for FLAMES Game"
setup(
    name='ARMflames',
    version='1.0.3',
    author='Abdurrahim',
    package=['ARMflames'],
    author_email='abdurrahim251103@gmail.com',
    description=d,
    long_description="FLAMES game of the programs",
    long_description_content_type='text/markdown',
    keywords=['FLAMES Game','Games','String','GUI'],
    license="MIT",
    packages=find_packages(),
    include_package_data=True,
    package_data={'': ['static/*']},
    classifiers=c,
    install_requires=['Rahimcalc'],
    url="https://pypi.org/user/AbdurRahim2003/",
    entry_points={'console_scripts':['ARMflames=ARMflames.Comments:comments']},
    project_urls=
    {
        'Source Code':'https://github.com/Abdurrahimgithub/Python_Package.git',
        'Documentation':'https://github.com/Abdurrahimgithub/Python_Package.git'
        }
    )
