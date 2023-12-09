from setuptools import setup, find_packages

setup(
    name='tybase2',
    version='0.0.1',
    description='一个简单的工具包',
    long_description=open('README.md', 'r', encoding='utf-8').read(),
    long_description_content_type='text/markdown',
    author='Ty',
    author_email='zhangtezhangte@gmail.com',
    # url='https://github.com/yourusername/your_package',
    packages=find_packages(),
    install_requires=[
        # List your package dependencies here
    ],
#     classifiers='Development Status3 - Alpha',
# 'Intended Audience :: Developers',
# 'License :: OSI Approved :: MIT License',
# 'Programming Language :: Python :: 3',
# 'Programming Language :: Python :: 3.6',
# 'Programming Language :: Python :: 3.7',
# 'Programming Language :: Python :: 3.8',
# 'Programming Language :: Python :: 3.9',,
)