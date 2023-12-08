import setuptools

PACKAGE_NAME = "profile-user-local"
package_dir = PACKAGE_NAME.replace("-", "_")

with open('README.md') as f:
    readme = f.read()

setuptools.setup(
    name=PACKAGE_NAME,
    version='0.0.7',  # https://pypi.org/project/profile-user-local/
    author="Circles",
    author_email="info@circles.life",
    description="PyPI Package for Circles profile-user Local Python",
    long_description=readme,
    long_description_content_type="text/markdown",
    url="https://github.com/circles",
    packages=[package_dir],
    package_dir={package_dir: f'{package_dir}/src'},
    package_data={package_dir: ['*.py']},
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: Other/Proprietary License",
        "Operating System :: OS Independent",
    ],
    install_requires=[
        'PyMySQL>=1.0.2',
        'pytest>=7.4.0',
        'mysql-connector>=2.2.9',
        'logzio-python-handler>= 4.1.0',
        'user-context-remote>=0.0.17',
        'python-sdk-local>=0.0.27',
        'multipledispatch>=1.0.0'
    ],
)
