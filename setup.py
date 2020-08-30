from setuptools import setup, find_packages


setup(
    name='splatcoder',
    version='0.0.0',
    description="Template generation tool for atcoder.jp.",
    long_description=open('README.md').read(),
    long_description_content_type="text/markdown",
    packages=find_packages(),
    scripts=['bin/splat'],
    include_package_data=True,
    python_requires='>=3.6',
    install_requires=[
        'termcolor>=1.1.0',
        'jinja2>=1.0.0',
    ],
    author='ryomazda',
    url='https://github.com/RyoMazda/splatcoder',
    license="Apache",
)
