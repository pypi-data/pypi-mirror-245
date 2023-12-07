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
    'version': '0.0.3',
    'description': 'Gemini - Pytorch',
    'long_description': '[![Multi-Modality](agorabanner.png)](https://discord.gg/qUtxnK2NMf)\n\n# Gemini\n\n![gemini](gemini.png)\n\nThe open source implementation of Gemini, the model that will "eclipse ChatGPT", it seems to work by directly taking in all modalities without an encoder for some kind which means that the encoding is built into the modal.\n\ninput sequences {texts, audio, imgs, video} -> [tokens] -> transformer -> conditional decoding for img gen\n\nThis architecture looks very similiar to Fuyu\'s architecture just extended to many modalities, where instead of an vit encoder you just pass in the img embeddings into the transformer.\n\nThe token inputs to gemini will most likely be denoted by special modality tokens `[IMG] or <img> or [AUDIO] or <audio>`\n\nCodi also has conditional generation leverages the tokenized outputs.\n\nTo implement this, I plan to cover the img embedding first make sure that works well and then go onto the audio embeddings and then the video.\n\n\n# Install\n`pip3 install gemini-torch`\n\n\n## Usage\n\n### Gemini Transformer Usage\n- No multi-modal yet\n- Just language\n- Rope, xpos, alibi, etc, multi grouped queries, qk_norm\n```python\nimport torch \nfrom gemini_torch import Gemini\n\n# Initialize the model\nmodel = Gemini(\n    num_tokens=50432,\n    max_seq_len=8192,\n    dim=2560,\n    depth=32,\n    dim_head=128,\n    heads=24,\n    use_abs_pos_emb=False,\n    alibi_pos_bias=True,\n    alibi_num_heads=12,\n    rotary_xpos=True,\n    attn_flash=True,\n    attn_kv_heads=2,\n    qk_norm=True,\n    attn_qk_norm=True,\n    attn_qk_norm_dim_scale=True,\n)\n\n# Initialize the randint\nx = torch.randint(0, 50432, (1, 8192))\n\n# Apply model to y\ny = model(x)\n\n# Print logits\nprint(y)\n```\n--------\n\n### Multi-Modal with Imgs\n- Processes Img natively no encoders, we can definitely optimize this like Fuyu\n\n```python\nimport torch\nfrom gemini_torch.model import Gemini\n\n# Initialize model\nmodel = Gemini(\n    num_tokens=50432,\n    max_seq_len=8192,\n    dim=2560,\n    depth=32,\n    dim_head=128,\n    heads=24,\n    use_abs_pos_emb=False,\n    alibi_pos_bias=True,\n    alibi_num_heads=12,\n    rotary_xpos=True,\n    attn_flash=True,\n    attn_kv_heads=2,\n    qk_norm=True,\n    attn_qk_norm=True,\n    attn_qk_norm_dim_scale=True,\n)\n\n# Text shape: [batch, seq_len, dim]\ntext = torch.randint(0, 50432, (1, 8192))\n\n# Img shape: [batch, channels, height, width]\nimg = torch.randn(1, 3, 256, 256)\n\n# Apply model to text and img\ny = model(text, img)\n\n# Output shape: [batch, seq_len, dim]\nprint(y.shape)\n\n```\n------\n\n### `ImgToTransformer`\n- takes in img -> patches -> reshapes to [B, SEQLEN, Dim] to align with transformer\n```python\nimport torch\nfrom gemini_torch.utils import ImgToTransformer\n\n# Example usage\nnum_patches = 16\npatch_size = 16\ntransformer_dim = 512\nimg_channels = 3\nseq_len = 50000\nreduced_dim = 256  # Reduced dimension after dimensionality reduction\n\nmodel = ImgToTransformer(\n    num_patches, patch_size, transformer_dim, img_channels, seq_len, reduced_dim\n)\n\n# Dummy image input [BATCH, CHANNELS, HEIGHT, WIDTH]\ndummy_img = torch.randn(1, 3, 64, 64)  # Batch size of 1, 64x64 RGB image\n\n# Forward pass\nseq_space_output = model(dummy_img)\nprint(seq_space_output.shape)  # Expected shape: [1, 50000, 256]\n\n\n```\n\n\n# References\n* Combine Reinforcment learning with modular pretrained transformer, multi-modal capabilities, image, audio, \n* self improving mechanisms like robocat\n* PPO? or MPO\n* get good at backtracking and exploring alternative paths\n* speculative decoding\n* Algorithm of Thoughts\n* RLHF\n* [Gemini Report](https://storage.googleapis.com/deepmind-media/gemini/gemini_1_report.pdf)\n* [Gemini Landing Page](https://deepmind.google/technologies/gemini/#introduction)\n\n\n# Todo\n- [ ] Implement the img feature embedder and align imgs with text and pass into transformer\n- [ ] Implement the audio processing by making an audio processor that intakes in audio embeddings and reshapes it to match language embeddings dimension shape [B, SEQLEN, Dim]\n- [ ] Do the same for video',
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
