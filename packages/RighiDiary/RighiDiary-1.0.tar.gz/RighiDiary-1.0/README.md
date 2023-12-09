
[![MIT License](https://img.shields.io/badge/License-MIT-green.svg)](https://github.com/Komo4ekoI/RighiDiaryAPI/blob/master/LICENSE/) [![wakatime](https://wakatime.com/badge/user/90c8afe4-47c1-4f14-9423-4474ab0618ae/project/018c3029-0cbb-4c30-a3a6-3eb80dfefcc1.svg)](https://wakatime.com/badge/user/90c8afe4-47c1-4f14-9423-4474ab0618ae/project/018c3029-0cbb-4c30-a3a6-3eb80dfefcc1)

## INFO

This library makes it easy to retrieve data from a Mastercom account for `Liceo Shientifico A. Righi (Cesena)`.

All operations are performed using http requests and data scraping using the `beautifulsoup4` library. I had to use scraping because Mastercom does not have a full API, so some operations can be a bit slow.

Any operations can be performed with a login and password from Mastercom account.

In some cases you may get false data or a library error because I can take into account all possible scenarios of Mastercom. The data from my account was taken into account during development, but the diary has features that I don't have access to.

If you find a bug and are willing to help improve the project, you can [write about it](https://github.com/Komo4ekoI/RighiDiaryAPI/issues).
## Documentation

#### In progress


## Installation

The library is available on PyPi, so you can install it in the standard way:

##### Windows
```bash
  pip install RighiDiary
```
##### Ubuntu/macOS
```bash
  pip3 install RighiDiary
```
## Example

```Python
from RighiDiary import authorize_user
import asyncio

my_password: str = "CoolPassword"
my_login: int = 123456


async def main():
    user = await authorize_user(login=my_login, password=my_password)
    print(user.full_name)
    print(user.agenda[0])

if __name__ == '__main__':
    asyncio.run(main())
```

