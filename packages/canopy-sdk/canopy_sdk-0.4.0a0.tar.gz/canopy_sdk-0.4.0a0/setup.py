# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src',
 'canopy_cli': 'src/canopy_cli',
 'canopy_cli.data_loader': 'src/canopy_cli/data_loader',
 'canopy_server': 'src/canopy_server',
 'canopy_server.models.v1': 'src/canopy_server/models/v1'}

packages = \
['canopy',
 'canopy.chat_engine',
 'canopy.chat_engine.history_pruner',
 'canopy.chat_engine.prompt_builder',
 'canopy.chat_engine.query_generator',
 'canopy.context_engine',
 'canopy.context_engine.context_builder',
 'canopy.knowledge_base',
 'canopy.knowledge_base.chunker',
 'canopy.knowledge_base.record_encoder',
 'canopy.knowledge_base.reranker',
 'canopy.llm',
 'canopy.models',
 'canopy.tokenizer',
 'canopy.utils',
 'canopy_cli',
 'canopy_cli.data_loader',
 'canopy_server',
 'canopy_server.models.v1']

package_data = \
{'': ['*']}

install_requires = \
['fastapi>=0.92.0,<0.93.0',
 'gunicorn>=21.2.0,<22.0.0',
 'jsonschema>=4.2.0,<5.0.0',
 'openai>=1.2.3,<2.0.0',
 'pandas-stubs>=2.0.3.230814,<3.0.0.0',
 'pandas==2.0.0',
 'pinecone-client==3.0.0.dev4',
 'pinecone-text>=0.7.0,<0.8.0',
 'prompt-toolkit>=3.0.39,<4.0.0',
 'pyarrow>=14.0.1,<15.0.0',
 'pydantic>=1.10.7,<2.0.0',
 'python-dotenv>=1.0.0,<2.0.0',
 'sentencepiece>=0.1.99,<0.2.0',
 'sse-starlette>=1.6.5,<2.0.0',
 'tenacity>=8.2.1,<9.0.0',
 'tiktoken>=0.3.3,<0.4.0',
 'tokenizers>=0.15.0,<0.16.0',
 'tqdm>=4.66.1,<5.0.0',
 'transformers>=4.35.2,<5.0.0',
 'types-jsonschema>=4.2.0,<5.0.0',
 'types-pyyaml>=6.0.12.12,<7.0.0.0',
 'types-tqdm>=4.61.0,<5.0.0',
 'uvicorn>=0.20.0,<0.21.0']

entry_points = \
{'console_scripts': ['canopy = canopy_cli.cli:cli']}

setup_kwargs = {
    'name': 'canopy-sdk',
    'version': '0.4.0a0',
    'description': 'Retrieval Augmented Generation (RAG) framework and context engine powered by Pinecone',
    'long_description': '# Canopy\n\n<p align="center">\n<a href="https://pypi.org/project/canopy-sdk" target="_blank">\n    <img src="https://img.shields.io/pypi/pyversions/canopy-sdk" alt="Supported Python versions">\n</a>\n<a href="https://pypi.org/project/canopy-sdk" target="_blank">\n    <img src="https://img.shields.io/pypi/v/canopy-sdk?label=pypi%20package" alt="Package version">\n</a>\n</p>\n\n\n**Canopy** is an open-source Retrieval Augmented Generation (RAG) framework and context engine built on top of the Pinecone vector database. Canopy enables you to quickly and easily experiment with and build applications using RAG. Start chatting with your documents or text data with a few simple commands.   \n\nCanopy takes on the heavy lifting for building RAG applications: from chunking and embedding your text data to chat history management, query optimization, context retrieval (including prompt engineering), and augmented generation. \n\nCanopy provides a configurable built-in server so you can effortlessly deploy a RAG-powered chat application to your existing chat UI or interface. Or you can build your own, custom RAG application using the Canopy library. \n\nCanopy lets you evaluate your RAG workflow with a CLI based chat tool. With a simple command in the Canopy CLI you can interactively chat with your text data and compare RAG vs. non-RAG workflows side-by-side. \n\nCheck out our [blog post](https://pinecone.io/blog/canopy-rag-framework) to learn more, or see a quick [tutorial here](https://www.youtube.com/watch?v=dVGPglKh80Y). \n\n## RAG with Canopy\n\n![](.readme-content/rag_flow.png)\n\nCanopy implements the full RAG workflow to prevent hallucinations and augment your LLM with your own text data.\n\nCanopy has two flows: knowledge base creation and chat. In the knowledge base creation flow, users upload their documents and transform them into meaningful representations stored in Pinecone\'s Vector Database. In the chat flow, incoming queries and chat history are optimized to retrieve the most relevant documents, the knowledge base is queried, and a meaningful context is generated for the LLM to answer.\n\n## What\'s inside the box?\n\n1. **Canopy Core Library** - The library has 3 main classes that are responsible for different parts of the RAG workflow:\n    * **ChatEngine** - Exposes a chat interface to interact with your data. Given the history of chat messages, the `ChatEngine` formulates relevant queries to the `ContextEngine`, then uses the LLM to generate a knowledgeable response.\n    * **ContextEngine**  - Performs the “retrieval” part of RAG. The `ContextEngine` utilizes the underlying `KnowledgeBase` to retrieve the most relevant documents, then formulates a coherent textual context to be used as a prompt for the LLM. \n    * **KnowledgeBase** - Manages your data for the RAG workflow. It automatically chunks and transforms your text data into text embeddings, storing them in a Pinecone vector database. Given a text query - the `KnowledgeBase` will retrieve the most relevant document chunks from the database. \n\n\n> More information about the Core Library usage can be found in the [Library Documentation](docs/library.md)\n\n2. **Canopy Server** - This is a webservice that wraps the **Canopy Core** library and exposes it as a REST API. The server is built on top of FastAPI, Uvicorn and Gunicorn and can be easily deployed in production. \nThe server also comes with a built-in Swagger UI for easy testing and documentation. After you [start the server](#3-start-the-canopy-server), you can access the Swagger UI at `http://host:port/docs` (default: `http://localhost:8000/docs`)\n\n 3. **Canopy CLI** - A built-in development tool that allows users to swiftly set up their own Canopy server and test its configuration.  \nWith just three CLI commands, you can create a new Canopy server, upload your documents to it, and then interact with the Chatbot using a built-in chat application directly from the terminal. The built-in chatbot also enables comparison of RAG-infused responses against a native LLM chatbot.\n\n## Setup\n\n0. set up a virtual environment (optional)\n```bash\npython3 -m venv canopy-env\nsource canopy-env/bin/activate\n```\n> More information about virtual environments can be found [here](https://docs.python.org/3/tutorial/venv.html)\n\n1. install the package\n```bash\npip install canopy-sdk\n```\n\n2. Set up the environment variables\n\n```bash\nexport PINECONE_API_KEY="<PINECONE_API_KEY>"\nexport PINECONE_ENVIRONMENT="<PINECONE_ENVIRONMENT>"\nexport OPENAI_API_KEY="<OPENAI_API_KEY>"\nexport INDEX_NAME="<INDEX_NAME>"\n```\n\n<details>\n<summary><b><u>CLICK HERE</u></b> for more information about the environment variables \n\n<br /> \n</summary>\n\n| Name                  | Description                                                                                                                 | How to get it?                                                                                                                                                               |\n|-----------------------|-----------------------------------------------------------------------------------------------------------------------------|------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|\n| `PINECONE_API_KEY`    | The API key for Pinecone. Used to authenticate to Pinecone services to create indexes and to insert, delete and search data | Register or log into your Pinecone account in the [console](https://app.pinecone.io/). You can access your API key from the "API Keys" section in the sidebar of your dashboard |\n| `PINECONE_ENVIRONMENT`| Determines the Pinecone service cloud environment of your index e.g `west1-gcp`, `us-east-1-aws`, etc                       | You can find the Pinecone environment next to the API key in [console](https://app.pinecone.io/)                                                                             |\n| `OPENAI_API_KEY`      | API key for OpenAI. Used to authenticate to OpenAI\'s services for embedding and chat API                                    | You can find your OpenAI API key [here](https://platform.openai.com/account/api-keys). You might need to login or register to OpenAI services                                |\n| `ANYSCALE_API_KEY`    | API key for Anyscale. Used to authenticate to Anyscale Endpoints for open source LLMs                                    | You can register Anyscale Endpoints and find your API key [here](https://app.endpoints.anyscale.com/)\n| `INDEX_NAME`          | Name of the Pinecone index Canopy will underlying work with                                                                  | You can choose any name as long as it follows Pinecone\'s [restrictions](https://support.pinecone.io/hc/en-us/articles/11729246212637-Are-there-restrictions-on-index-names-#:~:text=There%20are%20two%20main%20restrictions,and%20emojis%20are%20not%20supported.)                                                                                       |\n| `CANOPY_CONFIG_FILE` | The path of a configuration yaml file to be used by the Canopy server. | Optional - if not provided, default configuration would be used |\n</details>\n\n\n3. Check that installation is successful and environment is set, run:\n```bash\ncanopy\n```\n\nOutput should be similar to this:\n\n```bash\nCanopy: Ready\n\nUsage: canopy [OPTIONS] COMMAND [ARGS]...\n# rest of the help message\n```\n\n## Quickstart\n\nIn this quickstart, we will show you how to use the **Canopy** to build a simple question answering system using RAG (retrieval augmented generation).\n\n### 1. Create a new **Canopy** Index\n\nAs a one-time setup, Canopy needs to create a new Pinecone index that is configured to work with Canopy, just run:\n\n```bash\ncanopy new\n```\n\nAnd follow the CLI instructions. The index that will be created will have a prefix `canopy--<INDEX_NAME>`.   \nYou only have to do this process once for every Canopy index you want to create.\n\n> To learn more about Pinecone indexes and how to manage them, please refer to the following guide: [Understanding indexes](https://docs.pinecone.io/docs/indexes)\n\n### 2. Uploading data\n\nYou can load data into your Canopy index using the command:\n\n```bash\ncanopy upsert /path/to/data_directory\n# or\ncanopy upsert /path/to/data_directory/file.parquet\n# or\ncanopy upsert /path/to/data_directory/file.jsonl\n# or\ncanopy upsert /path/to/directory_of_txt_files/\n# ...\n```\n\nCanopy supports files in `jsonl`, `parquet` and `csv` formats. Additionally, you can load plaintext data files in `.txt` format. In this case, each file will be treated as a single document. The document id will be the filename, and the source will be the full path of the file. \n\n> **Note**: Document fields are used in the RAG flow and should comply with the following schema:\n\n```bash\n+----------+--------------+--------------+---------------+\n| id(str)  | text(str)    | source       | metadata      |\n|          |              | Optional[str]| Optional[dict]|\n|----------+--------------+--------------+---------------|\n| "id1"    | "some text"  | "some source"| {"key": "val"}|\n+----------+--------------+--------------+---------------+\n\n# id       - unique identifier for the document\n#\n# text     - the text of the document, in utf-8 encoding.\n#\n# source   - the source of the document, can be any string, or null.\n#            ** this will be used as a reference in the generated context. **\n#\n# metadata - optional metadata for the document, for filtering or additional context.\n#            Dict[str, Union[str, int, float, List[str]]]\n```\n\n[This notebook](https://colab.research.google.com/github/pinecone-io/examples/blob/master/learn/generation/canopy/00-canopy-data-prep.ipynb) shows how you create a dataset in this format, Follow the instructions in the CLI when you upload your data.\n\n### 3. Start the Canopy server\n\nThe Canopy server exposes Canopy\'s functionality via a REST API. Namely, it allows you to upload documents, retrieve relevant docs for a given query, and chat with your data. The server exposes a `/chat.completion` endpoint that can be easily integrated with any chat application.\nTo start the server, run:\n\n```bash\ncanopy start\n```\nNow, you should be prompted with the following standard Uvicorn message:\n```\n...\n\nINFO:     Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)\n```\n**That\'s it!** you can now start using the **Canopy** server with any chat application that supports a `/chat.completion` endpoint.\n\n> The canopy start command will keep the terminal occupied (recommended use). \n> If you want to run the server in the background, you can use the following command - **```nohup canopy start &```**\n\n\n### Stopping the server \nTo stop the server, simply press `CTRL+C` in the terminal where you started it.\n\nIf you have started the server in the background, you can stop it by running:\n\n```bash\ncanopy stop\n```\n\n## Evaluation chat tool\n\nCanopy\'s CLI comes with a built-in chat app that allows you to interactively chat with your text data and compare RAG vs. non-RAG workflows side-by-side to evaluate the results\n\nIn a new terminal window, set the [required environment variables](#setup) then run:\n\n```bash \ncanopy chat\n```\n\nThis will open a chat interface in your terminal. You can ask questions and the RAG-infused chatbot will try to answer them using the data you uploaded.\n\nTo compare the chat response with and without RAG use the `--no-rag` flag\n\n> **Note**: This method is only supported with OpenAI at the moment.\n\n```bash\ncanopy chat --no-rag\n```\n\nThis will open a similar chat interface window, but will show both the RAG and non-RAG responses side-by-side.\n\n## Considerations\n\n* Canopy currently only supports OpenAI as the backend for both the embedding model and the LLM. Rate limits and pricing set by OpenAI will apply.  \n* More integrations will be supported in the near future.\n\n## Advanced usage\n\n### Migrating an existing OpenAI application to **Canopy**\n\nIf you already have an application that uses the OpenAI API, you can migrate it to **Canopy** by simply changing the API endpoint to `http://host:port/v1`, for example with the default configuration:\n\n```python\nimport openai\n\nopenai.api_base = "http://localhost:8000/v1"\n\n# now you can use the OpenAI API as usual\n```\n\nor without global state change:\n\n```python\nimport openai\n\nopenai_response = openai.Completion.create(..., api_base="http://localhost:8000/v1")\n```\n\n### Running Canopy server in production\n\nCanopy is using FastAPI as the web framework and Uvicorn as the ASGI server. It is recommended to use Gunicorn as the production server, mainly because it supports multiple worker processes and can handle multiple requests in parallel, more details can be found [here](https://www.uvicorn.org/deployment/#using-a-process-manager).\n\nTo run the canopy server for production, please run:\n\n```bash\ngunicorn canopy_cli.app:app --worker-class uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000 --workers <number of desired worker processes>\n```\n\nThe server interacts with services like Pinecone and OpenAI using your own authentication credentials. When deploying the server on a public web hosting provider, it is recommended to enable an authentication mechanism, so that your server would only take requests from authenticated users.\n',
    'author': 'Relevance Team',
    'author_email': 'relevance@pinecone.io',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<3.13',
}


setup(**setup_kwargs)
