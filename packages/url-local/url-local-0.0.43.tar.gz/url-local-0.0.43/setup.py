import setuptools

PACKAGE_NAME = "url-local"
package_dir = PACKAGE_NAME.replace("-", "_")

setuptools.setup(
    name=PACKAGE_NAME,  
    version='0.0.43', # https://pypi.org/project/url-local

    author="Circles",
    author_email="info@circles.life",
    url=f"https://github.com/circles-zone/{PACKAGE_NAME}-python-package",
    packages=[package_dir],
    package_dir={package_dir: f'{package_dir}/src'},
    package_data={package_dir: ['*.py']},
    long_description="URL Local",
    long_description_content_type='text/markdown',
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: Other/Proprietary License",
        "Operating System :: OS Independent",
    ],
    install_requires=[
        "python-dotenv>=1.0.0",
        "pytest>=7.4.1",
        "database-without-orm-local>=0.0.79",
        "logger-local>=0.0.59",
        "queue-local>=0.0.13"
    ]
)
