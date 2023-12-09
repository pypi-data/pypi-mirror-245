import logging, os, random, json, base64

from .Tokenizer import Tokenizer

class ModelCardReader:
    @classmethod
    def read_model_from_path(cls, path, override_dic=None):
        print(path)
        with open(path, 'r',encoding="utf-8") as file:
            dic = json.load(file)
            if override_dic is not None:
                for key, value in override_dic.items():
                    logging.info("MODELCARD_READER OVERRIDE PARAMETER "+key)
                    dic[key] = value
            return dic

    @classmethod
    def read_from_server(cls, model_card_id, override_dic=None):
        assert 0
        return character_dic


class ModelGenerator:
    def __init__(self, model_folder_path, override_dic={}):
        self.model_cards = {}
        for model in os.listdir(model_folder_path):
            card = None
            if model.lower().endswith(".json"):
                model_json_path = os.path.join(model_folder_path, model)
                config = ModelCardReader.read_model_from_path(path=model_json_path, override_dic=override_dic)
                if 'version' in config.keys():
                    if float(config['version']) == 2:
                        card = ModelCardV2(**config)

                if card is None:
                    logging.error("모델 카드 버전을 확인할 수 없습니다.")
                    raise Exception
                self.model_cards[card.name] = card

    def model(self, model_name):
        if model_name in self.model_cards.keys():
            return self.model_cards[model_name]
        else:
            model_info = ModelCardReader.read_from_server(model_name)
            model = ModelCardV2(**model_info)
            self.model_cards[model_name] = model
            return model



class ModelCardV2:
    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)

    def get_random_messages(self, messages):
        return random.choice(messages)

    def num_tokens_from_messages(self, messages):
        return Tokenizer.num_tokens_from_messages(messages=messages, backend=self.model_backend)
