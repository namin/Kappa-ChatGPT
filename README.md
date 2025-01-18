# Kappa ChatGPT actions

This repo develops GPT actions for ChatGPT to support Kappa simulations.
It attempts to support longer-running simulations by separating actions to start a simulation and to fetch the results, when available.

It uses the [KappaTools](https://github.com/Kappa-Dev/KappaTools) project, which must be installed in a sibling directory. The Python environment for the Kappa simulator should be in a Python environment called `kappa-env` in that sibling `KappaTools` directory.

## Installation of Kappa on Linux

- `sudo apt-get install opam`
- `opam init --compile=4.14.1`
- `git clone https://github.com/Kappa-Dev/KappaTools.git`
- `opam install --deps-only .`
- `dune build`
- `python3 -m venv kappa-env`
- `source kappa-env/bin/activate`
- `pip install .`

## Deployment of ChatGPT action

The deployment steps follow this [HOWTO](https://github.com/namin/io-chatgpt.livecode.ch/tree/main/deploy), using the configurations here (in `kappa-chatgpt.service`, replace `namin` with your username).
