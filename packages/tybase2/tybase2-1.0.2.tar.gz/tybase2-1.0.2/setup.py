from setuptools import setup, find_packages

setup(
    name='tybase2',
    version='1.0.2',
    description='给视频添加水印',
    long_description=open('README.md', 'r', encoding='utf-8').read(),
    long_description_content_type='text/markdown',
    author='Ty',
    author_email='zhangtezhangte@gmail.com',
    # url='https://github.com/yourusername/your_package',
    packages=find_packages(),
    install_requires=[
        # List your package dependencies here
    ],
)