from setuptools import setup, find_packages

setup(
    name="wlgenlib",
    version="0",
    packages=find_packages(),
    install_requires=[
        "simpy",
        "loguru",
        "omegaconf",
        "numpy",
        "setuptools",
    ],
    package_data={'': ['*.json']},
    license='MIT',
    description = 'Simulating arrival of tasks/data into a system',
    url = 'https://github.com/columbia/workload-generator',
    download_url = "https://github.com/columbia/workload-generator/archive/refs/tags/v0.tar.gz",
)
