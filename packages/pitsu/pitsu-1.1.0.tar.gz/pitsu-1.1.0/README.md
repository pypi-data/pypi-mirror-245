# pitsu
a python module to create html pages with python code

# how to use
```the register process it's blocked in pypi so i only can upload in test pypi and may be some uninstable```

* instal pitsu:

```bash
pip3 install -i https://test.pypi.org/simple/ pitsu
```

or 

```bash
pip install -i https://test.pypi.org/simple/ pitsu
```

simple example:

```python
from pitsu import *

html(
    head(
        meta(charset='UTF-8'),
        title('Example Login')
    ),
    body(
        form(
            inp( # inp = input element
                type='text',
                name='user',
                id='user',
                required=True
            ),
            br(),
            inp(
                type='password',
                name='pass',
                id='pass',
                required=True
            ),
            br(),
            inp(
                type='submit',
                value='Submit'
            ),
            action='/',
            method='get'
        )
    ),
    lang='en'
).pack()
```

output:
```html
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>
Example Login
</title>
</head>
<body>
<form action="/" method="get">
<input type="text" name="user" id="user" required>
<br>
<input type="password" name="pass" id="pass" required>
<br>
<input type="submit" value="Submit">
</form>
</body>
</html>
```
