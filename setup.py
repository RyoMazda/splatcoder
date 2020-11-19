from setuptools import setup, find_packages


setup(
    name='splatcoder',
    version='0.0.1',
    description="Template generation tool for atcoder.jp.",
    long_description=open('README.md').read(),
    long_description_content_type="text/markdown",
    packages=find_packages(
        exclude=[
            "*.tests",
            "*.tests.*",
            "tests.*",
            "tests",
        ]
    ),
    scripts=['bin/splat'],
    include_package_data=True,
    python_requires='>=3.8',
    install_requires=[
        'pyyaml',
        'requests',
        'termcolor>=1.1.0',
        'jinja2>=1.0.0',
        'beautifulsoup4>=4.9.1',
    ],
    author='ryomazda',
    url='https://github.com/RyoMazda/splatcoder',
    license="Apache",
)
