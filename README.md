# Kappa ChatGPT actions

This repo develops GPT actions for ChatGPT to support Kappa simulations.
It attemps to support longer-running simulations by separating actions to start a simulation and to fetch the results, when available.

It uses the [KappaTools](https://github.com/namin/io-chatgpt.livecode.ch/tree/main/deploy) project, which must be installed in a sibling directory. The Python environment for the Kappa simulator should be in a Python environment called `kappa-env` in that sibling `KappaTools` directory.

The deployment steps follow this [HOWTO](https://github.com/namin/io-chatgpt.livecode.ch/tree/main/deploy).
