"""xAI Software Development Kit (SDK).

This SDK lets you interact with the xAI API. In order to access the API, you need to generate an
API key in our IDE, which is available under ide.x.ai. After signing in, click on your username in
the top right hand corner and select "API Keys". Generate a new API key and make sure to assign the
correct ACLs. In order to sample from the model, you need the `chat:write` or `sampler:write` ACLs.
"""

from .client import Client
