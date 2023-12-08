import setuptools

with open("README.md", "r") as f:
	description = f.read()

setuptools.setup(
	#meta-data
	name='quantumsecurity',
	version='0.0.4',
	author='Rajesh Harinarayan',
	author_email='rajeshtceit@gmail.com',
	description='A package for supporting security applications with the power of quantum computing and cyrptography',
	packages=setuptools.find_packages(),
	classifiers=[
		"Programming Language :: Python :: 3",
		"License :: OSI Approved :: MIT License",
		"Operating System :: OS Independent",
	],
	python_requires='>=3.7',
        long_description = description,
        long_description_content_type = "text/markdown",
)
