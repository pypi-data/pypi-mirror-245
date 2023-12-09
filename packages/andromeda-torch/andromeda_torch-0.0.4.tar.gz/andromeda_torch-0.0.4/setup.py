# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['andromeda_torch', 'andromeda_torch.core', 'andromeda_torch.utils']

package_data = \
{'': ['*']}

install_requires = \
['SentencePiece',
 'accelerate',
 'datasets',
 'deepspeed',
 'einops',
 'lion-pytorch',
 'matplotlib',
 'numpy',
 'torch',
 'transformers']

setup_kwargs = {
    'name': 'andromeda-torch',
    'version': '0.0.4',
    'description': 'Andromeda - Pytorch',
    'long_description': '[![Multi-Modality](images/agorabanner.png)](https://discord.gg/qUtxnK2NMf)\n\n\n# Andromeda: Ultra-Fast and Ultra-Intelligent SOTA Language Model 🚀🌌\n\n<div align="center">\n\n[![Open Bounties](https://img.shields.io/endpoint?url=https%3A%2F%2Fconsole.algora.io%2Fapi%2Fshields%2Fkyegomez%2Fbounties%3Fstatus%3Dopen)](https://console.algora.io/org/kyegomez/bounties?status=open)\n[![Rewarded Bounties](https://img.shields.io/endpoint?url=https%3A%2F%2Fconsole.algora.io%2Fapi%2Fshields%2Fkyegomez%2Fbounties%3Fstatus%3Dcompleted)](https://console.algora.io/org/kyegomez/bounties?status=completed)\n[![GitHub issues](https://img.shields.io/github/issues/kyegomez/Andromeda)](https://github.com/kyegomez/Andromeda/issues) \n[![GitHub forks](https://img.shields.io/github/forks/kyegomez/Andromeda)](https://github.com/kyegomez/Andromeda/network) \n[![GitHub stars](https://img.shields.io/github/stars/kyegomez/Andromeda)](https://github.com/kyegomez/Andromeda/stargazers) \n[![GitHub license](https://img.shields.io/github/license/kyegomez/Andromeda)](https://github.com/kyegomez/Andromeda/blob/main/LICENSE)\n[![Share on Twitter](https://img.shields.io/twitter/url/https/twitter.com/cloudposse.svg?style=social&label=Share%20%40kyegomez/Andromeda)](https://twitter.com/intent/tweet?text=Check%20out%20this%20amazing%20AI%20project:%20Andromeda&url=https%3A%2F%2Fgithub.com%2Fkyegomez%2FAndromeda) \n[![Share on Facebook](https://img.shields.io/badge/Share-%20facebook-blue)](https://www.facebook.com/sharer/sharer.php?u=https%3A%2F%2Fgithub.com%2Fkyegomez%2FAndromeda) \n[![Share on LinkedIn](https://img.shields.io/badge/Share-%20linkedin-blue)](https://www.linkedin.com/shareArticle?mini=true&url=https%3A%2F%2Fgithub.com%2Fkyegomez%2FAndromeda&title=&summary=&source=)\n![Discord](https://img.shields.io/discord/999382051935506503)\n[![Share on Reddit](https://img.shields.io/badge/-Share%20on%20Reddit-orange)](https://www.reddit.com/submit?url=https%3A%2F%2Fgithub.com%2Fkyegomez%2FAndromeda&title=Andromeda%20-%20the%20next%20generation%20AI%20shields) \n[![Share on Hacker News](https://img.shields.io/badge/-Share%20on%20Hacker%20News-orange)](https://news.ycombinator.com/submitlink?u=https%3A%2F%2Fgithub.com%2Fkyegomez%2FAndromeda&t=Andromeda%20-%20the%20next%20generation%20AI%20shields) \n[![Share on Pinterest](https://img.shields.io/badge/-Share%20on%20Pinterest-red)](https://pinterest.com/pin/create/button/?url=https%3A%2F%2Fgithub.com%2Fkyegomez%2FAndromeda&media=https%3A%2F%2Fexample.com%2Fimage.jpg&description=Andromeda%20-%20the%20next%20generation%20AI%20shields) \n[![Share on WhatsApp](https://img.shields.io/badge/-Share%20on%20WhatsApp-green)](https://api.whatsapp.com/send?text=Check%20out%20Andromeda%20-%20the%20next%20generation%20AI%20shields%20%23Andromeda%20%23AI%0A%0Ahttps%3A%2F%2Fgithub.com%2Fkyegomez%2FAndromeda)\n\n</div>\n\n\n\nWelcome to Andromeda, The Fastest, Most Creative, and Reliable Language Model Ever Built, train your own verison, conduct inference, and finetune your own verison with simple plug in and play scripts get started in 10 seconds:\n\n## Features\n\n- 💼 Handle Ultra Long Sequences (32,000-200,000+ context lengths)\n- ⚡ Ultra Fast Processing (32,000+ tokens in under 100ms)\n- 🎓 Superior Reasoning Capabilities\n\n## 🎯 Principles\n\n- **Efficiency**: Optimize with techniques like attention flashing, rotary position encodings, and deep normalization.\n- **Flexibility**: Adapt to various tasks and domains for wide applications.\n- **Scalability**: Designed to scale with resources and data sizes.\n- **Community-Driven**: Thrives on contributions from the open-source community.\n\n---\n\n\n## 💻 Install\n\n`pip install TheBestLLMEver`\n\n\n## Usage\n```python\nimport torch\n\nfrom andromeda.configs import Andromeda1Billion\n\nmodel = Andromeda1Billion()\n\nx = torch.randint(0, 256, (1, 1024)).cuda()\n\nout = model(x)  # (1, 1024, 20000)\nprint(out)\n\n\n```\n\n## 📚 Training\n\n1. Set the environment variables:\n   - `ENTITY_NAME`: Your wandb project name\n   - `OUTPUT_DIR`: Directory to save the weights (e.g., `./weights`)\n   - `MASTER_ADDR`: For distributed training\n   - `MASTER_PORT` For master port distributed training\n   - `RANK`- Number of nodes services\n   - `WORLD_SIZE` Number of gpus\n\n2. Configure the training:\n   - Accelerate Config\n   - Enable Deepspeed 3\n   - Accelerate launch train_distributed_accelerate.py\n\nFor more information, refer to the [Training SOP](DOCs/TRAINING.md).\n\n---\n\n\n## Todo\n- [ ] add truncated rope from https://arxiv.org/abs/2308.10882\n\n- [ ] add rope from code llama\n\n- [ ] multi grouped query \n\n-  [ ] LLM Infinite for long sequence generation https://arxiv.org/pdf/2308.16137.pdf\n\n- [ ] speculative decoder \n\n\n---\n\n## 📈 Benchmarks\n\n### Speed\n- Andromeda utilizes one of the most reliable Attentions ever, flash attention 2.0 Triton. It consumes 50x less memory than GPT-3 and 10x less than LLAMA.\n\n![AndromedaBanner](images/andromeda_performance.png)\n\n- We can speed this up even more with dynamic sparse flash attention 2.0.\n\n---\n\n# 🔮 Join the Journey\n\nWe\'re just getting started, and we invite you to join the journey. Let\'s revolutionize the NLP landscape together! 🚀🌟\n\n- Join Agora and work with 2,000+ AI Engineers to implement all new features.\n- Provide compute and help train Andromeda.\n- Share the message on how we\'re liberating this superintelligent AI and seizing the power from the corrupt, providing it back to you.\n',
    'author': 'Kye Gomez',
    'author_email': 'kye@apac.ai',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/kyegomez/Andromeda',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
