from setuptools import setup

setup(
    name="metamodel",
    version="0.3.0",
    author="stackdump",
    author_email="myork@stackdump.com",
    description="declare and simulate Petri-nets using python",
    license='MIT',
    keywords='pflow petri-net statemachine',
    packages=['metamodel'],
    install_requires='',
    long_description="""
    This library used to declare and simulate Petri-net models.
    """,
    url="https://pflow.dev/metamodel-py",
    classifiers=[
        "Development Status :: 4 - Beta",
        "License :: OSI Approved :: MIT License"
    ],
)
