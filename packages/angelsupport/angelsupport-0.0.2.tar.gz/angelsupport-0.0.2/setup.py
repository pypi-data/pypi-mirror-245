from setuptools import setup, find_packages

setup(
    name='angelsupport',
    version='0.0.2',
    description='Angel Support Program',
    author='Anthony',
    author_email='webmaster@ailike.me',
    url='https://ailike.me',
    install_requires=['openai', 'tiktoken'],
    packages=find_packages(exclude=[]),
    keywords=[],
    python_requires='>=3.6',
    package_data={},
    zip_safe=False,
    classifiers=[
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
    ],
)
