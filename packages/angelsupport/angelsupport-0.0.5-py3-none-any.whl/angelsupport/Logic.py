
from abc import *
import time, logging, json
from .Prompt import Prompt
from .GPTRequest import RawChatGPTQueue, GPTRequest
class AbstractLogic(metaclass=ABCMeta):
    def __init__(self, model_card, add_welcome_message=True, unique_id="SEOWOO_V2", version=2, creator="SW",
                 gpt_queue=None):
        logging.basicConfig(level=logging.INFO)
        self.unique_id = unique_id
        self.version = version
        self.creator = creator

        logging.info("[%s] %s에 의해 제작된 채팅 처리 로직 (VERSION %d)" % (unique_id, creator, version))
        logging.info("CHARACTER CARD ID : %s" % model_card.name)

        self.model_card = model_card
        self.model_card_id = model_card.name

        logging.info("모델 카드")
        logging.info(self.model_card)
        self.messages = []
        self.gpt_queue = gpt_queue

        if add_welcome_message:
            self.messages.append(Prompt.from_dict(self.model_card.get_random_messages(self.model_card.messages_welcome)))

        if gpt_queue is None:
            self.gpt_queue = RawChatGPTQueue(num_workers=1)


        self.logs = {}
        self.log_index = 0


    def reset_messages(self):
        self.messages.clear()


    def request_gpt(self, request_dic):
        self.log_index = self.log_index + 1
        self.logs["request_"+str(self.log_index)] = request_dic

        print(json.dumps(request_dic,indent=4,ensure_ascii=False))

        request = GPTRequest(request_dic)
        self.gpt_queue.q.put(request)

        while True:
            time.sleep(0.1)
            if request.status == "FINISHED":
                response = request.response
                self.logs["response_" + str(self.log_index)] = response
                del request
                print(json.dumps(response, indent=4, ensure_ascii=False))
                return response

            if request.status == "ERROR":
                return None

    @abstractmethod
    def process(self, user_input_text):
        pass

    def register_assistant_text(self, assistant_response_text, hidden_input_text=""):
        self.messages.append(Prompt(role='assistant',content=assistant_response_text, hidden_content=hidden_input_text))
        return assistant_response_text, hidden_input_text

    def register_user_input_text(self, user_input_text, hidden_input_text=""):
        self.messages.append(Prompt(role='user',content=user_input_text,hidden_content=hidden_input_text))
        return user_input_text, hidden_input_text

