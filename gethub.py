import requests, json


class GetGithubData:
    """
    receives a link from a repository in github and tries to 
    turn the link in a valid api link, makes the first call 
    for basic information, and the second to get the languages 
    used. Returns the first as a key-value pair and the 
    second as a list
    """

    def __init__(self, link):
        self.link_api = link

    def format_link(self, link):
        """
        format the received link, ex: github.com/owner/repository
        if the link no starts with https protocol, insert this,
        if the link ends with "/", remove this,
        insert "api." and "repos/" in its necessary position,
        and returns two urls, for basic info and languages used
        """
        link_api = link
        if not link_api.startswith("https://"):
            link_api = f"https://{link_api}"

        if link_api.endswith("/"):
            link_api = link_api[:-1]

        link_api = link_api.replace("://", "://api.")
        link_api = link_api.replace(".com/", ".com/repos/")

        link_api_langs = f"{link_api}/languages"

        return link_api, link_api_langs

    def get_basic_data(self, content):
        """
        get some basic infos and return a dict object
        """
        basic_data = {
            "name": content["name"],
            "owner": content["owner"]["login"],
            "link": content["html_url"],
            "link_api": content["url"],
            "description": content.get("description", "No description."),
            "stars": content["stargazers_count"],
        }

        return basic_data

    def get_langs(self, content):
        """
        get languages used in the project
        and return a list
        """
        langs = []

        for lang in content.keys():
            langs.append(lang)

        return langs

    def request_api(self):
        """
        call the format_link method to format and
        assign the two api urls, call the apis, if 
        status_code == 200, call the get_basic_data
        and get_langs with the formated links, and return
        a dict with basic data and a list with the langs
        if status_code is not 200, return None
        """
        link_api, link_api_langs = self.format_link(self.link_api)
        res = requests.get(link_api)
        res_langs = requests.get(link_api_langs)

        if res.status_code == 200 and res_langs.status_code == 200:
            basic_data = self.get_basic_data(json.loads(res.content))
            langs = self.get_langs(json.loads(res_langs.content))
            return basic_data, langs
        else:
            return None

repository = input("Insert the github repository url: ")
instance = GetGithubData(repository)
basic, langs = instance.request_api()

print("\nBasic informations: ")
for k, v in basic.items():
    print(f"{k} -> {v}")

print("\nUsed languages: ")
i = 1
for v in langs:
    print(f"{i} -> {v}")
    i += 1