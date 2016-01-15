from setuptools import setup, find_packages

setup(
	name='main',
	version='0.1',
	url='http://host/',
	author='author',
	author_email='email',
	packages=find_packages(),
	include_package_data=True,
	scripts=['manage.py'],
	install_requires=(
		'django<1.7',
	)
)
