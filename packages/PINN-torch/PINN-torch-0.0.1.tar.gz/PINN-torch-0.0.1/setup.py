from setuptools import setup, find_packages


# with open("README.md", "r") as fh:
#     long_description = fh.read()
    
    

setup(
    name="PINN-torch",
    version="0.0.1",
    description="PYPI tutorial package for PINN frameworks",
    author="johnjaejunlee95",
    author_email="johnjaejunlee@gmail.com",
    # url="https://github.com/johnjaejunlee95/PINN-torch",
    install_requires=[
        "tqdm",
        "numpy",
        "scikit-learn",
        'torch>=1.6.0',
        'deepxde'
    ],
    packages=find_packages(exclude=[]),
    keywords=["johnjaejunlee", "PINN", "Neural Netowrks", "pypi"],
    python_requires=">=3.8",
    package_data={},
    zip_safe=False,
    classifiers=[
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
    ],
)