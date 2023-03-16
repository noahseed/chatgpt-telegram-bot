#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""ChatGPT Telegram Bot

Description to be added.

__author__ = Zhiquan Wang
__copyright__ = Copyright 2023
__version__ = 1.2.2
__maintainer__ = Zhiquan Wang
__email__ = contact@flynmail.com
__status__ = Dev
"""

import openai, json, os
import datetime

class OpenAIParser:

    config_dict = {}

    def __init__(self):
        # load config
        with open("config.json") as f:
            self.config_dict = json.load(f)
        # init openai
        # openai.organization = self.config_dict["ORGANIZATION"] if "ORGANIZATION" in self.config_dict else "Personal"
        openai.api_key = self.config_dict["openai_api_key"]

    def _get_single_response(self, message):
        response = openai.ChatCompletion.create(model = "gpt-3.5-turbo",
                                            messages = [
                                                {"role": "system", "content": "Tu es un assistant virtuel utile, tu t'appelles TynnieBot. Ton rôle est d'aider "
                                                 "les bénévoles de l'ONG Alliances Célestes Internationales (https://www.alliances-celestes-internationales.com/) "
						 "ainsi que de sa filiale française, l'ONG Alliances Célestes France (https://www.alliances-celestes.com/Accueil/). "
						 "Ces deux sites web sont ta principale source d'informations, base tes réponses sur leur contenu."},
                                                {"role": "user", "content": message}
                                            ])
        return response["choices"][0]["message"]["content"]

    def get_response(self, userid, context_messages):
        context_messages.insert(0, {"role": "system", "content": "Tu es un assistant virtuel utile, tu t'appelles TynnieBot. Ton rôle est d'aider "
                                    "les bénévoles de l'ONG Alliances Célestes Internationales (https://www.alliances-celestes-internationales.com/) "
                                    "ainsi que de sa filiale française, l'ONG Alliances Célestes France (https://www.alliances-celestes.com/Accueil/). "
                                    "Ces deux sites web sont ta principale source d'informations, base tes réponses sur leur contenu."})
        try:
            response = openai.ChatCompletion.create(model = "gpt-3.5-turbo",
                                                messages = context_messages)
            return (response["choices"][0]["message"]["content"], response["usage"]["total_tokens"])
        except Exception as e:
            return (str(e) + "\nDésolé, je ne me sens pas bien. Veuillez réessayer.", 0)

    def speech_to_text(self, userid, audio_file):
        # transcript = openai.Audio.transcribe("whisper-1", audio_file, language="zh")
        transcript = openai.Audio.transcribe("whisper-1", audio_file)
        return transcript["text"]

    def image_generation(self, userid, prompt):
        response = openai.Image.create(prompt = prompt, n=1, size = "512x512", user = userid)
        image_url = response["data"][0]["url"]
        # for debug use
        # image_url = "https://catdoctorofmonroe.com/wp-content/uploads/2020/09/iconfinder_cat_tied_275717.png"
        usage = 1 # reserve for future use
        return (image_url, usage)

if __name__ == "__main__":
    openai_parser = OpenAIParser()
    # print(openai_parser._get_single_response("Tell me a joke."))
    print(openai_parser.get_response("123", [{"role": "user", "content": "Raconte moi une blague."}]))
