from setuptools import find_packages, setup

with open("README.md") as readme_file:
    README = readme_file.read()

setup_args = {
    "name": "shopcloud-django-authenticator",
    "version": "1.13.0",
    "description": "A Module for single sign in",
    "long_description_content_type": "text/markdown",
    "long_description": README,
    "license": "MIT",
    "packages": find_packages(),
    "author": "Konstantin Stoldt",
    "author_email": "konstantin.stoldt@talk-point.de",
    "url": "https://github.com/Talk-Point/shopcloud-django-authenticator",
}

install_requires = [
    "Django>=3.2",
    "djangorestframework",
    "django-filter",
    "markdown",
    "pyjwt",
]

if __name__ == "__main__":
    setup(**setup_args, install_requires=install_requires)
