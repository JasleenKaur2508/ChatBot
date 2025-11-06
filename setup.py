from setuptools import setup, find_packages

setup(
    name="nlp-chatbot",
    version="1.0.0",
    packages=find_packages(),
    install_requires=[
        "streamlit>=1.27.0",
        "openai>=0.28.1,<1.0.0",
        "python-dotenv>=1.0.0"
    ],
    entry_points={
        "console_scripts": [
            "chatbot=app:main",
        ],
    },
    python_requires=">=3.8",
    author="Jasleen Kaur",
    author_email="jasleenkaur@example.com",
    description="A friendly NLP chatbot powered by OpenAI",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/JasleenKaur2508/chatbot",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: End Users/Desktop",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
)