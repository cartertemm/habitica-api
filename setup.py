from setuptools import setup, find_packages

setup(
	name="habitica-api",
	version="0.1",
	packages=find_packages(),
	url="https://github.com/cartertemm/habitica-api",
	license="MIT",
	author="Carter Temm",
	author_email="cartertemm@gmail.com",
	description="A natural, feature rich Python client over the Habitica API",
	long_description=open("README.md").read(),
	long_description_content_type="text/markdown",
	install_requires=[i for i in open("requirements.txt").read().splitlines() if i],
	classifiers=[
		"Development Status :: 3 - Alpha",
		"Intended Audience :: Developers",
		"License :: OSI Approved :: MIT License",
		"Programming Language :: Python :: 3",
		"Programming Language :: Python :: 3.6",
		"Programming Language :: Python :: 3.7",
		"Programming Language :: Python :: 3.8",
		"Programming Language :: Python :: 3.9",
	],
)
