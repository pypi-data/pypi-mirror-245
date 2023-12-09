# loopsapi
Python wrapper for Loops.so API

#### Install
```
pip3 install loopsapi
```

### Example
```Python
import os
import loopsapi

API_KEY = os.environ['LOOPS_API_KEY']

api = loopsapi.Loops(api_key=API_KEY)
test = api.apikey.test()
print(print)
```

## Classes and methods
```
Loops.apikey.test - Test if API KEY is valid

Loops.custom_fields.list - List custom fields

Loops.transactional_emails.send - Send transactional email

Loops.events.send - Send event

Loops.contacts.find - Find contact
Loops.contacts.create - Create contact
Loops.contacts.update - Update contact
Loops.contacts.delete - Delete contact
```
