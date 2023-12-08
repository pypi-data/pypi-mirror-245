from setuptools import setup
import platform

install_requires = [
    "pypdf",
    "langchain==0.0.345",
    "chromadb==0.4.14",
    "openai==0.27",
    "tiktoken",
    "lark==1.1.7",
    "scikit-learn<1.3.0",
    "jieba==0.42.1",
    "sentence-transformers==2.2.2",
    "torch==2.0.1",
    "transformers==4.31.0",
    "llama-cpp-python==0.2.6",
    "auto-gptq==0.3.1",
    "tqdm==4.65.0",
    "docx2txt==0.8",
    "rouge==1.0.1",
    "rouge-chinese==1.0.3",
    "bert-score==0.3.13",
    "click",
    "tokenizers==0.13.3",
    "streamlit==1.28.2",
    "streamlit_option_menu==0.3.6",
]
if platform.system() == "Windows":
    install_requires.append("opencc==1.1.1")
else:
    install_requires.append("opencc==1.1.6")

setup(
    name="akasha-terminal",
    version="0.8",
    description="document QA package using langchain and chromadb",
    long_description="""Akasha simplifies document-based Question Answering (QA) by harnessing the power of Large Language Models to accurately answer your queries while searching through your provided documents.
With Akasha, you have the flexibility to choose from a variety of language models, embedding models, and search types. Adjusting these parameters is straightforward, allowing you to optimize your approach and discover the most effective methods for obtaining accurate answers from Large Language Models.""",
    author="chih chuan chang",
    url="https://gitlab-devops.iii.org.tw/root/qaiii-1",
    author_email="ccchang@iii.org.tw",
    install_requires=install_requires,
    packages=["akasha", "akasha.models", "cli", "akasha.eval", "akasha.summary", "akasha.interface"],
    entry_points={"console_scripts": ["akasha = cli.glue:akasha"]},
    python_requires=">=3.8"
)
