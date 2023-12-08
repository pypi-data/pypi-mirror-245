import os

import setuptools

with open("README.md", "r") as fh:
	long_description = fh.read()

about = {}

with open(os.path.join("django_graphene_permissions", "__version__.py")) as f:
    exec(f.read(), about)

setuptools.setup(
	name="django_graphene_permissions_redux",
	version=about["__version__"],
	author="Max Ettelson",
	author_email="mdettelson@gmail.com",
	description="DRF like permission system for django graphene",
	license='BSD',
	long_description=long_description,
	long_description_content_type="text/markdown",
	url="https://github.com/mdettelson/django-graphene-permissions-redux",
	packages=setuptools.find_packages(),
	classifiers=[
		"License :: OSI Approved :: BSD License",
		"Programming Language :: Python",
		"Programming Language :: Python :: 3",
		"Framework :: Django",
		"Operating System :: OS Independent",
	],
)
