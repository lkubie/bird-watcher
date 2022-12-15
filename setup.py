import setuptools

packages = setuptools.find_packages()
packages.append("")

setuptools.setup(name='bird-watcher',
      version='0.0.1', #Use Semantic Versioning
      python_requires=">=3.7",
      packages=packages,
      description='Use a Raspberry Pi + webcam to watch for birds and get an alert when you see one. Maybe with AI recognition?!',
      author='Lenore Kubie, Ashley Boucher',
      author_email='',
      install_requires=["picamerax", "opencv-python"],
     )