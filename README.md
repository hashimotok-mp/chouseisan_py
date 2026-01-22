# chouseisan_py (Unofficial Fork)

This is an **unofficial fork** of  
[ryu22e/chouseisan_py](https://github.com/ryu22e/chouseisan_py).

This fork fixes issues caused by recent changes to  
[調整さん](https://chouseisan.com/) and adds improvements for event creation.

Original project:
Copyright (c) 2021–2024 Ryuji Tsutsui  
Licensed under the MIT License.

---

## Overview

`chouseisan_py` automates the operations of  
[調整さん](https://chouseisan.com/) (Chouseisan).

Currently supported features:

- Create events
- Login-required event creation
- (Fork) Updated page parsing to match current Chouseisan behavior

---

## Installation (GitHub)

⚠ This fork is **not published on PyPI**.  
Please install it directly from GitHub.

```bash
pip install git+https://github.com/hashimotok-mp/chouseisan_py.git
```
If you want to install a specific branch:
```bash
pip install git+https://github.com/hashimotok-mp/chouseisan_py.git@master
```

---

## Usage
```py
from datetime import datetime
from chouseisan_py.chouseisan import Auth, Chouseisan

auth = Auth(
    email="test@example.com",
    password="your_password"
)

chouseisan = Chouseisan(auth)

url = chouseisan.create_event(
    title="test event",
    candidate_days=[
        datetime(2021, 10, 17, 19, 0),
        datetime(2021, 10, 18, 19, 0),
    ],
)

print(url)
```

---

## Differences from Original
- Fixed login and CSRF token handling
- Updated selectors for event creation
- Compatible with current Chouseisan HTML structure

---

## License
MIT License
See `LICENSE` file for details.

This project includes and modifies software originally developed by
Ryuji Tsutsui.