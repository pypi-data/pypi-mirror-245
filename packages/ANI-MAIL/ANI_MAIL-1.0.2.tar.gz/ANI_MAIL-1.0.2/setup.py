from setuptools import setup

def readme():
    with open('README.md') as f:
        README = f.read()
    return README


setup(
    name="ANI_MAIL",
    version="1.0.2",
    description="A Python package to send mail one person or more than one person, read mail, clear inbox, clear trash box and you can mail bomb as well.",
    long_description=readme(),
    long_description_content_type="text/markdown",
    url="https://github.com/aniket-coder-arch/Email_Manager",
    author="Aniket Dubey",
    author_email="daniket182@gmail.com",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
    ],
    packages=["Ani_mail"],
    include_package_data=True,
    install_requires=[""],
    entry_points={
        "console_scripts": [
            "ANI_MAIL=Ani_mail.EmailManager:Email_Manager",
        ]
    },
)