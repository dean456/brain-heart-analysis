# SETUP SCRIPT

import setuptools
from pyhrv import __author__, __version__, __email__, name, description

# Create setup
setuptools.setup(
	name=name,
	version=__version__,
	author=__author__,
	author_email=__email__,
	description=description,
	long_description='',
	long_description_content_type="text/markdown",
	python_requires='>=3.8',
	url="https://github.com/dean456/brain-heart-analysis",
	keywords=['Heart Rate Variability', 'HRV','EEG'],
	setup_requires=[
		'numpy',
		'scipy',
		'biosppy',
		'matplotlib',
		'nolds',
		'spectrum',
	],
	install_requires=[
		'biosppy',
		'matplotlib',
		'numpy',
		'scipy',
		'nolds',
		'spectrum',
	],

	packages=setuptools.find_packages(),
	package_data={},
	include_package_data=True,
	classifiers=[
		'Intended Audience :: Developers',
		'Intended Audience :: Education',
		'Intended Audience :: Science/Research',
		'Natural Language :: English',
		'License :: OSI Approved :: BSD License',
		'Programming Language :: Python',
		'Programming Language :: Python :: 2.7',
		'Programming Language :: Python :: 3.4',
		'Programming Language :: Python :: 3.5',
		'Programming Language :: Python :: 3.6',
		'Programming Language :: Python :: 3.7',
		'Operating System :: OS Independent',
	],
)