---
title: Overview
---

**Approzium** enables services to securely connect to databases without providing credentials. Passwords don't even live
in your client's memory, so your client can't leak them!

Here's how you might typically connect to your database.
```python
from psycopg2 import connect

conn = connect("host=1.2.3.4 user=user1 password=verySecurePassword")
```

Here's what it would look like with Approzium. 😎
```python
import approzium
from approzium.psycopg2 import connect

approzium.default_auth_client = approzium.AuthClient('authenticator:6001')
conn = connect("host=1.2.3.4 user=user1")  # Look ma, no password!
```

You can get started with Approzium [here](/quickstart).

Learn how it works by checking out the [architecture](/architecture).

We hope you like it! 🤗