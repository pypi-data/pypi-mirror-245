from setuptools import setup, find_packages

setup(
    name="wlgen-lib",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "simpy",
        "loguru",
        "omegaconf",
        "numpy",
        "setuptools",
    ],
    license='MIT',
    description = 'Simulating arrival of tasks/data into a system',
    url = 'https://github.com/columbia/workload-generator',
    download_url = "https://github.com/columbia/workload-generator/archive/refs/tags/v1.0.0.tar.gz",
)
