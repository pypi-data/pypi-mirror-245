"""
Setup script for the bishop-bridge package.
"""
from setuptools import find_packages, setup

setup(
    name="bishop-bridge",
    version="0.0.2",
    description="A package for creating a Bishop bridge",
    url="https://github.com/CalvaryDesign/bishop-bridge",
    author="Noah Hunn",
    author_email="nhunn@calvaryrobotics.com",
    packages=find_packages(exclude=['examples', 'tests']),
    install_requires=["python-socketio", "msgpack"],
)
