# Flask Session using Azure table storage (Using Azure-Data-Tables Library)


[![PyPI - License](https://img.shields.io/pypi/l/flask-session-azure)](https://pypi.org/project/flask-session-azure/)
[![PyPI](https://img.shields.io/pypi/v/flask-session-azure)](https://pypi.org/project/flask-session-azure/)
![PyPI - Python Version](https://img.shields.io/pypi/pyversions/flask-session-azure)

This module can be used as a Flask Session handler for Azure table storage or Azure CosmosDB.
All stored data is encrypted using AES encryption.

Example usage:

```python
import flask
from flask_session_azure import storage_account_interface

app = flask.Flask(__name__)
app.secret_key = "MyVerySecretEnryptionKeyForEverything" # must be at least 16 characters, the longer the better
connection_string = "DefaultEndpointsProtocol=https;AccountName=someAccount;AccountKey=someKey;EndpointSuffix=core.windows.net"
app.session_interface = storage_account_interface(connection_string)
```

This will store the session data in a table called `flasksession`, with a partition key called `default_session`. IF the table does not yet exists, it will be created the first time a session is stored.
You can overwrite these default when creating the session interface:
```python
app.session_interface = storage_account_interface(connection_string, table_name="mytablename", partition_key="app1", create_table_if_not_exists=False)
```

If you use this in Azure Function, or Azure Web-Service, you most certainly already have a storage account connection in your environment variable `AzureWebJobsStorage`:
```python
import os
import flask
from flask_session_azure import storage_account_interface

app = flask.Flask(__name__)
app.secret_key = "MyVerySecretEnryptionKeyForEverything" # must be at least 16 characters, the longer the better
connection_string = os.environ.get("AzureWebjobsStorage")
app.session_interface = storage_account_interface(connection_string)
```

## Changelog

### 0.4.5
- Edited functions to use updated Azure-Core library instead of deprecated Azure-Common. Updated flask elements to use newer app.config format.

### 0.4.4
- Edited functions to use the Azure-Data-Tables library that is actively maintained by Microsoft

### 0.4.3
- Fixed issue with secret key length and secret key containing non-asci characters

### 0.4.2
- Fixed issue if "samesite" cookie value was not set (i.e. set to none). If it is not set, it is now set to Lax to work in an azure function (see https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Set-Cookie/SameSite)

### 0.4.1
- First public release
