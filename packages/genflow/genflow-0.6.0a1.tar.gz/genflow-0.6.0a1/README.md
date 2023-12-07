<!-- Title -->

# ⛓️ Genflow

~ An effortless way to experiment and prototype [LangChain](https://github.com/hwchase17/langchain) pipelines ~

<p>
<img alt="GitHub Contributors" src="https://img.shields.io/github/contributors/aiplanethub/genflow" />
<img alt="GitHub Last Commit" src="https://img.shields.io/github/last-commit/aiplanethub/genflow" />
<img alt="" src="https://img.shields.io/github/repo-size/aiplanethub/genflow" />
<img alt="GitHub Issues" src="https://img.shields.io/github/issues/aiplanethub/genflow" />
<img alt="GitHub Pull Requests" src="https://img.shields.io/github/issues-pr/aiplanethub/genflow" />
<img alt="Github License" src="https://img.shields.io/github/license/aiplanethub/genflow" />
</p>

<p>
<a href="https://discord.gg/EqksyE2EX9"><img alt="Discord Server" src="https://dcbadge.vercel.app/api/server/EqksyE2EX9?compact=true&style=flat"/></a>
<a href="https://huggingface.co/spaces/aiplanet/Genflow"><img src="https://huggingface.co/datasets/huggingface/badges/raw/main/open-in-hf-spaces-sm.svg" alt="HuggingFace Spaces"></a>
</p>

<a href="https://github.com/aiplanethub/genflow">
    <img width="100%" src="https://github.com/aiplanethub/genflow/blob/dev/img/genflow-demo.gif?raw=true"></a>

<p>
</p>

# Table of Contents

- [⛓️ Genflow](#️-genflow)
- [Table of Contents](#table-of-contents)
- [📦 Installation](#-installation)
  - [Locally](#locally)
  - [HuggingFace Spaces](#huggingface-spaces)
- [🖥️ Command Line Interface (CLI)](#️-command-line-interface-cli)
  - [Usage](#usage)
    - [Environment Variables](#environment-variables)
- [Deployment](#deployment)
  - [Deploy Genflow on Google Cloud Platform](#deploy-genflow-on-google-cloud-platform)
  - [Deploy on Railway](#deploy-on-railway)
  - [Deploy on Render](#deploy-on-render)
- [🎨 Creating Flows](#-creating-flows)
- [👋 Contributing](#-contributing)
- [📄 License](#-license)

# 📦 Installation

### <b>Locally</b>

You can install Genflow from pip:

```shell
# This installs the package without dependencies for local models
pip install genflow
```

To use local models (e.g llama-cpp-python) run:

```shell
pip install genflow[local]
```

This will install the following dependencies:

- [CTransformers](https://github.com/marella/ctransformers)
- [llama-cpp-python](https://github.com/abetlen/llama-cpp-python)
- [sentence-transformers](https://github.com/UKPLab/sentence-transformers)

You can still use models from projects like LocalAI

Next, run:

```shell
python -m genflow
```

or

```shell
genflow run # or genflow --help
```

### HuggingFace Spaces

You can also check it out on [HuggingFace Spaces](https://huggingface.co/spaces/aiplanet/Genflow) and run it in your browser! You can even clone it and have your own copy of Genflow to play with.

# 🖥️ Command Line Interface (CLI)

Genflow provides a command-line interface (CLI) for easy management and configuration.

## Usage

You can run the Genflow using the following command:

```shell
genflow run [OPTIONS]
```

Each option is detailed below:

- `--help`: Displays all available options.
- `--host`: Defines the host to bind the server to. Can be set using the `GENFLOW_HOST` environment variable. The default is `127.0.0.1`.
- `--workers`: Sets the number of worker processes. Can be set using the `GENFLOW_WORKERS` environment variable. The default is `1`.
- `--timeout`: Sets the worker timeout in seconds. The default is `60`.
- `--port`: Sets the port to listen on. Can be set using the `GENFLOW_PORT` environment variable. The default is `7860`.
- `--config`: Defines the path to the configuration file. The default is `config.yaml`.
- `--env-file`: Specifies the path to the .env file containing environment variables. The default is `.env`.
- `--log-level`: Defines the logging level. Can be set using the `GENFLOW_LOG_LEVEL` environment variable. The default is `critical`.
- `--components-path`: Specifies the path to the directory containing custom components. Can be set using the `GENFLOW_COMPONENTS_PATH` environment variable. The default is `genflow/components`.
- `--log-file`: Specifies the path to the log file. Can be set using the `GENFLOW_LOG_FILE` environment variable. The default is `logs/genflow.log`.
- `--cache`: Selects the type of cache to use. Options are `InMemoryCache` and `SQLiteCache`. Can be set using the `GENFLOW_LANGCHAIN_CACHE` environment variable. The default is `SQLiteCache`.
- `--dev/--no-dev`: Toggles the development mode. The default is `no-dev`.
- `--path`: Specifies the path to the frontend directory containing build files. This option is for development purposes only. Can be set using the `GENFLOW_FRONTEND_PATH` environment variable.
- `--open-browser/--no-open-browser`: Toggles the option to open the browser after starting the server. Can be set using the `GENFLOW_OPEN_BROWSER` environment variable. The default is `open-browser`.
- `--remove-api-keys/--no-remove-api-keys`: Toggles the option to remove API keys from the projects saved in the database. Can be set using the `GENFLOW_REMOVE_API_KEYS` environment variable. The default is `no-remove-api-keys`.
- `--install-completion [bash|zsh|fish|powershell|pwsh]`: Installs completion for the specified shell.
- `--show-completion [bash|zsh|fish|powershell|pwsh]`: Shows completion for the specified shell, allowing you to copy it or customize the installation.

### Environment Variables

You can configure many of the CLI options using environment variables. These can be exported in your operating system or added to a `.env` file and loaded using the `--env-file` option.

A sample `.env` file named `.env.example` is included with the project. Copy this file to a new file named `.env` and replace the example values with your actual settings. If you're setting values in both your OS and the `.env` file, the `.env` settings will take precedence.

# Deployment

## Deploy Genflow on Google Cloud Platform

Follow our step-by-step guide to deploy Genflow on Google Cloud Platform (GCP) using Google Cloud Shell. The guide is available in the [**Genflow in Google Cloud Platform**](GCP_DEPLOYMENT.md) document.

Alternatively, click the **"Open in Cloud Shell"** button below to launch Google Cloud Shell, clone the Genflow repository, and start an **interactive tutorial** that will guide you through the process of setting up the necessary resources and deploying Genflow on your GCP project.

[![Open in Cloud Shell](https://gstatic.com/cloudssh/images/open-btn.svg)](https://console.cloud.google.com/cloudshell/open?git_repo=https://github.com/aiplanethub/genflow&working_dir=scripts&shellonly=true&tutorial=walkthroughtutorial_spot.md)

## Deploy on Railway

[![Deploy on Railway](https://railway.app/button.svg)](https://railway.app/template/JMXEWp?referralCode=MnPSdg)

## Deploy on Render

<a href="https://render.com/deploy?repo=https://github.com/aiplanethub/genflow/tree/main">
<img src="https://render.com/images/deploy-to-render-button.svg" alt="Deploy to Render" />
</a>

# 🎨 Creating Flows

Creating flows with Genflow is easy. Simply drag sidebar components onto the canvas and connect them together to create your pipeline. Genflow provides a range of [LangChain components](https://langchain.readthedocs.io/en/latest/reference.html) to choose from, including LLMs, prompt serializers, agents, and chains.

Explore by editing prompt parameters, link chains and agents, track an agent's thought process, and export your flow.

Once you're done, you can export your flow as a JSON file to use with LangChain.
To do so, click the "Export" button in the top right corner of the canvas, then
in Python, you can load the flow with:

```python
from genflow import load_flow_from_json

flow = load_flow_from_json("path/to/flow.json")
# Now you can use it like any chain
flow("Hey, have you heard of Genflow?")
```

# 👋 Contributing

We welcome contributions from developers of all levels to our open-source project on GitHub. If you'd like to contribute, please check our [contributing guidelines](./CONTRIBUTING.md) and help make Genflow more accessible.

---

Join our [Discord](https://discord.com/invite/EqksyE2EX9) server to ask questions, make suggestions and showcase your projects! 🦾

<p>
</p>

[![Star History Chart](https://api.star-history.com/svg?repos=aiplanethub/genflow&type=Timeline)](https://star-history.com/#aiplanethub/genflow&Date)

# 📄 License

Genflow is released under the MIT License. See the LICENSE file for details.
