import setuptools
# Each Python project should have pyproject.toml or setup.py
# used by python -m build
# ```python -m build``` needs pyproject.toml or setup.py
# The need for setup.py is changing as of poetry 1.1.0 (including current pre-release) as we have moved away from
# needing to generate a setup.py file to enable editable installs - We might able to delete this file in the near future

PACKAGE_NAME = "profile-instagram-local"
package_dir = PACKAGE_NAME.replace("-", "_")

setuptools.setup(
    name=PACKAGE_NAME,
    version='0.0.14',  # https://pypi.org/project/profile-instagram-local
    author="Circles",
    author_email="info@circles.life",
    packages=[package_dir],
    package_dir={package_dir: f'{package_dir}/src'},
    package_data={package_dir: ['*.py']},
    description="PyPI Package for Circles profile-instagram-graphql-imp-local-python-package Local Python",
    long_description="This is a package for importing data from Instagram business accounts.",
    long_description_content_type="text/markdown",
    url="https://github.com/circles",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: Other/Proprietary License",
        "Operating System :: OS Independent",
    ],
    install_requires=["logger-local>=0.0.11",
                      "requests>=2.26.0",
                      "python-sdk-local>=0.0.27",
                      "user-context-remote>=0.0.21",
                      "url-local>=0.0.37",
                      "profile-local>=0.0.35",
                      "user-external-local>=0.0.32"]
 )
