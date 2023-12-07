from setuptools import setup, find_packages

setup(
    name='telcolib',
    version='0.1',
    packages=find_packages(),
    description='A phone number validation library for multiple countries',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/yourusername/telcolib',
    author='Don Johnson',
    author_email='dj@codetestcode.io',
    license='MIT',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Libraries',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
    ],
    keywords='phone number validation telecommunications',
    install_requires=[
        # Add dependencies here
    ],
    python_requires='>=3.6',
)
