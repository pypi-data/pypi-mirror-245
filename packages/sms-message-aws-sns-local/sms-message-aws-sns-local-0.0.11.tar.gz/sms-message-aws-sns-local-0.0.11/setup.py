import setuptools
# Each Python project should have pyproject.toml or setup.py (if both exist, we use the setup.py)
# TODO: Please create pyproject.toml instead of setup.py (delete the setup.py)
# used by python -m build
# ```python -m build``` needs pyproject.toml or setup.py
# The need for setup.py is changing as of poetry 1.1.0 (including current pre-release)
# as we have moved away from needing to generate a setup.py file to enable editable installs -
# We might able to delete this file in the near future
PACKAGE_NAME = "sms-message-aws-sns-local"
package_dir = PACKAGE_NAME.replace("-", "_")

setuptools.setup(
    name=PACKAGE_NAME,
    version='0.0.11',
    author="Circles",
    author_email="info@circlez.ai",
    description="PyPI Package for Circles AWS SMS",
    long_description="PyPI Package for Circles AWS SMS",
    long_description_content_type='text/markdown',
    url="https://github.com/circ-zone/sms-message-aws-local-python-package",
    packages=[package_dir],
    package_dir={package_dir: f'{package_dir}/src'},
    package_data={package_dir: ['*.py']},
    install_requires=["message-local", "api-management-local", "variable-local", "boto3>=1.28.70"],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: Other/Proprietary License",
        "Operating System :: OS Independent",
    ],
)
