from pathlib import Path

import setuptools

this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

setuptools.setup(
    name="st_stepper",
    version="0.0.2",
    author="tushar2704",
    author_email="tushar.27041994@gmail.com",
    description="Streamlit component -st_stepper",
    long_description="Streamlit componen -st_stepper",
    long_description_content_type="Streamlit component -st_stepper",
    url="",
    packages=setuptools.find_packages(),
    include_package_data=True,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent"
        ],
    keywords=['Python', 'Streamlit', 'React', 'JavaScript', 'Custom', 'www.tushar-aggarwal.com'],
    python_requires=">=3.7",
    install_requires=[
        # By definition, a Custom Component depends on Streamlit.
        # If your component has other Python dependencies, list
        # them here.
        "streamlit >= 0.63",
    ],
    extras_require={
        "devel": [
            "wheel",
            "pytest==7.4.0",
            "playwright==1.39.0",
            "requests==2.31.0",
            "pytest-playwright-snapshot==1.0",
            "pytest-rerunfailures==12.0",
        ]
    }
)
