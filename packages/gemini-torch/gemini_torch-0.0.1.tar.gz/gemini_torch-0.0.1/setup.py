# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['gemini_torch']

package_data = \
{'': ['*']}

install_requires = \
['einops', 'torch', 'torchvision', 'zetascale']

setup_kwargs = {
    'name': 'gemini-torch',
    'version': '0.0.1',
    'description': 'Gemini - Pytorch',
    'long_description': '[![Multi-Modality](agorabanner.png)](https://discord.gg/qUtxnK2NMf)\n\n# Gemini\n\n![gemini](gemini.png)\n\nThe open source implementation of Gemini, the model that will "eclipse ChatGPT", it seems to work by directly taking in all modalities without an encoder for some kind which means that the encoding is built into the modal.\n\ninput sequences {texts, audio, imgs, video} -> [tokens] -> transformer -> conditional decoding for img gen\n\nThis architecture looks very similiar to Fuyu\'s architecture just extended to many modalities, where instead of an vit encoder you just pass in the img embeddings into the transformer.\n\nThe token inputs to gemini will most likely be denoted by special modality tokens `[IMG] or <img> or [AUDIO] or <audio>`\n\nCodi also has conditional generation leverages the tokenized outputs.\n\nTo implement this, I plan to cover the img embedding first make sure that works well and then go onto the audio embeddings and then the video.\n\n\n\n\n\n\n# References\n* Combine Reinforcment learning with modular pretrained transformer, multi-modal capabilities, image, audio, \n* self improving mechanisms like robocat\n* PPO? or MPO\n* get good at backtracking and exploring alternative paths\n* speculative decoding\n* Algorithm of Thoughts\n* RLHF\n* ![Gemini Report](https://storage.googleapis.com/deepmind-media/gemini/gemini_1_report.pdf)\n* ![Gemini Landing Page](https://deepmind.google/technologies/gemini/#introduction)\n\n\n# Todo\n- [ ] Implement the img feature embedder and align imgs with text and pass into transformer\n',
    'author': 'Kye Gomez',
    'author_email': 'kye@apac.ai',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/kyegomez/Gemini',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
