# cashctrl
<u>Unofficial</u> python client for the [cashctrl api v1](https://app.cashctrl.com/static/help/en/api/index.html)

The goal was to make it easy, easier, easiest :smile::

```python
import cashctrl
cc=cashctrl.Client()
people=cc.person.list()
```



[TOC]



## Quickstart

### 1. Create role

It is recommended to create a seperate role for the admin user according to the [principle of least privilegue](https://en.wikipedia.org/wiki/Principle_of_least_privilege).![2023-09-22_11-08-29](assets/2023-09-22_11-08-29.png)

### 2. Create API-User

Now we can create the api user and copy the api-key:
![2023-09-22_11-15-17-5374206](assets/2023-09-22_11-15-17-5374206.png)

### 3. Add details to your environment

create the .env file and add your api-key, organization and language:

```bash
cp .env.example .env && open .env
```

**Make sure your .env file is safe**

### 4. have fun

```python
from cashctrl_py import CashCtrlClient
from icecream import ic

cc = CashCtrlClient()
people = cc.person.list()
ic(people)
```

## Contribute

### Fork

There is still much work to do 😔
If you want to contribute, please fork the repository and create a pull request.
`gh repo fork <USER>/cashctrl-py`

### Dynamic install

for development you can install the library dynamically with the following command:

```bash
pip3 install -e .
```

Now you can install it normally in other projects but the changes get reflected immediately.

### Swagger

there is an unofficial [swagger.json](./swagger.json) file to help with development. You can export it into your http-client i.e. [insomnia](https://insomnia.rest/).

### IDE

I used Vscode. You can install the recommended extensions when you first open the project:

![2023-09-22_11-51-06](assets/2023-09-22_11-51-06.png)