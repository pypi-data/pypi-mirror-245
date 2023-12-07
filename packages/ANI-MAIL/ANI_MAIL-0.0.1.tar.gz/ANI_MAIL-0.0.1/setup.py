from setuptools import setup

def readme():
    with open('README.md') as f:
        README = f.read()
    return README


setup(
    name="ANI_MAIL",
    version="0.0.1",
    description="A Python package to send mail, read mail and clear inbox.",
    long_description=readme(),
    long_description_content_type="text/markdown",
    url="",
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
            "ANI_MAIL=Ani_mail.mail:main",
        ]
    },
)