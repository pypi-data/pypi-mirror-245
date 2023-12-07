import os
import setuptools

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
README_PATH = os.path.join(ROOT_DIR, 'README.md')

setuptools.setup(
    name='quizium_prompt',
    version='0.0.1',
    author='dongwon.kim',
    author_email='dongwon.kim@riiid.co',

    description='Chapter, MCQ prompts',
    long_description=open(README_PATH, encoding='utf-8').read(),
    long_description_content_type='text/markdown',

    python_requires='>=3.11.3',
    license='MIT',
    url='https://github.com/riiid/quizium-prompt',
    py_modules=['quizium_prompt'],
    keywords=['quizium', 'prompt'],
    packages=setuptools.find_packages(),
    install_requires=['openai>=1.2.3'],
)
