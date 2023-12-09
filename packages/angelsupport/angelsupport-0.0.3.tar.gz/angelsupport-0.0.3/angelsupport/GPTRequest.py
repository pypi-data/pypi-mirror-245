import logging, json, traceback, time

class GPTRequest:
    def __init__(self, params):
        if type(params) is not dict:
            assert 0

        self.status = "PENDING"
        self.response = None
        self.request = params

class LogicTask:
    def __init__(self, model, messages):
        self.model = model
        self.messages = messages
        self.timestamp = time.time()

import queue, threading
from openai import OpenAI
class RawChatGPTQueue:
    DEBUG = False

    def __init__(self, num_workers, openai_key, openai_org):
        self.q = queue.Queue()
        self.num_workers = num_workers
        self.threads = []
        self.start_workers()
        self.client = OpenAI(
            api_key=openai_key,
            organization=openai_org
        )
    def query_gpt(self):
        while True:
            logging.debug("ChatGPTQueue %d개"%self.q.qsize())

            request = self.q.get()
            if request is None:
                break

            try:
                if request.status =="PENDING":
                    request.status = "REQUESTED"
                    dic = request.request
                    logging.debug("CHATGPT 요청")
                    logging.debug(json.dumps(dic,sort_keys=True, ensure_ascii=False, indent=4))
                    print(dic)

                    if dic.get('request_timeout',None) is not None:
                        dic['timeout'] = dic['request_timeout']
                        del dic['request_timeout']

                    response =  self.client.chat.completions.create(
                        **dic,
                    )
                    # for compatibility
                    response = {
                        'choices':[{
                            'message':{
                                'content':response.choices[0].message.content
                            }
                        }],
                        'model' : response.model,
                        'usage' : {
                            'completion_tokens' : response.usage.completion_tokens,
                            'prompt_tokens' : response.usage.prompt_tokens,
                            'total_tokens' : response.usage.total_tokens,
                        }
                    }

                    request.response = response
                    request.status = "FINISHED"

                    logging.debug("CHATGPT 회신")
                    logging.debug(response)

            except Exception as e:
                logging.error("CHATGPT 에러 발생 : " + str(e))
                logging.error(traceback.format_exc())
                request.status = "ERROR"

            self.q.task_done()

    def start_workers(self):
        threads = []
        for i in range(self.num_workers):
            t = threading.Thread(target=self.query_gpt)
            t.start()
            self.threads.append(t)
        return threads


    def stop_workers(self):
        # stop workers
        for i in self.threads:
            self.q.put(None)
        for t in self.threads:
            t.join()