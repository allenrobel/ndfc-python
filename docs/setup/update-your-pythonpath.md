# Update your PYTHONPATH

Update your PYTHONPATH to include both `ndfc-python` and `ansible-dcnm` repositories.

``` bash
export PYTHONPATH=$PYTHONPATH:$HOME/repos/ndfc-python/lib:$HOME/repos/ansible-dcnm
```

With the above in place, imports from the `ansible-dcnmn` repository will look
like the following in your `ndfc-python` scripts.

``` py title="Example imports"
from plugins.module_utils.common.rest_send import RestSend
from plugins.module_utils.common.sender_requests import Sender
```
