import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="hacku",
    version="1.2",
    author="0day",
    author_email="just@hacku.orz",
    description="hack u",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=setuptools.find_packages(),
    # 模块相关的元数据
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    # 依赖模块
    install_requires=[
        'beautifulsoup4',
        'loguru',
        'requests[socks]',
        'id-validator',
        'random-user-agent',
        'jieba',
        'pycryptodome',
        'rsa',
        'PyExecJS',
        'ujson',
        'shodan'
    ],
    python_requires='>=3',
)
