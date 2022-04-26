# SETUP SCRIPT

import setuptools

# Create setup
setuptools.setup(
	name='brain-heart-analysis',
	version=0.1,
	author="Dean Huang from Taiwan",
	author_email="dean4562007@gmail.com",
	description="a tool set for HRV and EEG analysis",
	long_description='as above',
	long_description_content_type="text/markdown",
	python_requires='>=3.8',
	url="https://github.com/dean456/brain-heart-analysis",
	keywords=['Heart Rate Variability', 'HRV','EEG'],
	setup_requires=[
		'pyHRV',
		'wfdb',
		'IPython',
		'numpy',
		'scipy',
		'biosppy',
		'matplotlib',
		'nolds',
		'spectrum',
	],
	install_requires=[
		'pyHRV',
		'wfdb',
		'IPython',
		'numpy',
		'scipy',
		'biosppy',
		'matplotlib',
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
		'Programming Language :: Python :: 3.8',
		'Operating System :: OS Independent',
	],
)
