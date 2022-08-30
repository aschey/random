import random
import string
import time
import requests
import re
import os
from dotenv import load_dotenv

load_dotenv()
astral_cookie = os.getenv("ASTRAL_COOKIE")
gh_cookie = os.getenv("GH_COOKIE")


repos = requests.get(
    "https://app.astralapp.com/api/stars", headers={"cookie": astral_cookie}
).json()

first = repos[0]

gh_repo = requests.get(
    f"https://api.github.com/repositories/{first['repo_id']}",
).json()

html_data = requests.get(
    f"https://github.com/{gh_repo['full_name']}/lists",
    headers={"cookie": gh_cookie},
).text.replace("\n", " ")
list_ids = re.findall(r'name="list_ids\[\]"\s+value="(\d+)"', html_data)
list_names = re.findall(r'class="Truncate-text">(\w+)</span>', html_data)

gh_lists = {pair[0]: pair[1] for pair in zip(list_names, list_ids)}

for repo in repos:
    repo_tags = [tag["name"] for tag in repo["tags"] if tag["name"] in gh_lists]
    if len(repo_tags) == 0:
        continue
    # for tag in repo_tags:
    gh_repo = requests.get(
        f"https://api.github.com/repositories/{repo['repo_id']}"
    ).json()
    list_ids = {f"list_ids[]": gh_lists[tag] for i, tag in enumerate(repo_tags)}
    session = requests.Session()
    boundary = "----WebKitFormBoundary" + "".join(
        random.sample(string.ascii_letters, 16)
    )

    html_data = requests.get(
        f"https://github.com/{gh_repo['full_name']}/lists",
        headers={"cookie": gh_cookie},
    ).text
    matches = re.findall(
        r'type="hidden" name="authenticity_token" value="([\w\-_]+)"',
        html_data,
    )

    authenticity_token = matches[0]
    headers = {
        "accept": "application/json",
        "content-type": f"multipart/form-data; boundary={boundary}",
        "cookie": gh_cookie,
    }

    ids_to_add = [
        f'--{boundary}\r\nContent-Disposition: form-data; name="list_ids[]"\r\n\r\n{gh_lists[tag]}\r\n'
        for tag in repo_tags
    ]
    ids_text = "".join(ids_to_add)

    data = f'--{boundary}\r\nContent-Disposition: form-data; name="_method"\r\n\r\nput\r\n--{boundary}\r\nContent-Disposition: form-data; name="authenticity_token"\r\n\r\n{authenticity_token}\r\n--{boundary}\r\nContent-Disposition: form-data; name="repository_id"\r\n\r\n{repo["repo_id"]}\r\n--{boundary}\r\nContent-Disposition: form-data; name="context"\r\n\r\nuser_list_menu\r\n--{boundary}\r\nContent-Disposition: form-data; name="list_ids[]"\r\n\r\n\r\n{ids_text}--{boundary}--\r\n'

    response = requests.post(
        f"https://github.com/{gh_repo['full_name']}/lists",
        headers=headers,
        data=data,
    )
    print(response)
    time.sleep(1)
