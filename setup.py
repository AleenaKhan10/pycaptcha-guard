import setuptools

setuptools.setup(
    name="pycaptcha-guard",
    version="0.1.5",
    author="AleenaMuskan",
    author_email="aleenakhanraees40@gmail.com",
    description="Solve any kind of captcha like human",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    license="MIT",
    packages=setuptools.find_packages(),
    install_requires=[
        "nopecha==1.0.8",
        "selenium==4.16.0",
        "pillow==10.1.0",
        "pyautogui==0.9.54"
    ],
    python_requires=">=3.9",
)