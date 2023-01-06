# nogging

Automatically use `nogging.yaml` to manage loggers.

## usage

```python
import logging

import nogging

nogging.Nogging().setup()

logger = logging.getLogger(__name__)

...
```
