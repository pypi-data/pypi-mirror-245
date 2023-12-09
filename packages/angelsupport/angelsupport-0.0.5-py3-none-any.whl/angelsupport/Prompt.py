import json, logging
from .Tokenizer import Tokenizer
__all__ = ['Prompt','PromptSection','GPTPrompt']

class Prompt:
    def __init__(self, role, content, hidden_content="", unique_id=None, backend="gpt-3.5-turbo-0613"):

        self.role = role
        self.content = content
        if hidden_content == "":
            hidden_content = content
        self.hidden_content  = hidden_content
        self.backend = backend
        self.unique_id = unique_id

        self.dic = {'role': role, 'content': content, 'hidden' :hidden_content}

    @classmethod
    def from_dict(cls, dict):
        return cls(**dict)

    @property
    def token(self):
        return Tokenizer.num_tokens_from_messages(self.dic, backend=self.backend)

    def __str__(self):
        return json.dumps(self.dic, sort_keys=True, ensure_ascii=False, indent=4)

    def __dict__(self):
        return {'role': self.role, 'content': self.content}

    def truncate_sentences(self, limit):
        if self.token <= limit:
            return
        sentences = self.content.split(". ")
        while True:
            if self.token <= limit:
                break
            sentences.pop(0)
            self.content = ". ".join(sentences)

    def __getstate__(self):
        return {'role':self.role,'content':self.content,'hidden_content':self.hidden_content,
                'unique_id':self.unique_id,'backend':self.backend}

    def __setstate__(self, d):
        self.role = d['role']
        self.content = d['content']
        self.hidden_content = d['hidden_content']
        self.unique_id = d['unique_id']
        self.backend = d['backend']


class PromptSection:
    def __init__(self, section, prompt=None, min_token=None, max_token=None):
        if prompt is None:
            prompt = []
        if type(prompt) is not list:
            prompt = [prompt]

        self.section = section
        self.prompt = prompt

        if max_token is not None:
            self.truncate(max_token)

        self.max_token = max_token
        self.min_token = min_token

        if max_token is not None and min_token is not None:
            assert max_token >= min_token

    def __len__(self):
        return len(self.prompt)

    @property
    def token(self):
        token = 0
        for p in self.prompt:
            token = token + p.token

        # print("%s - total %d - token %d"%(self.section,len(self.prompt),token))
        return token

    @property
    def num(self):
        return len(self.prompt)



    def truncate(self, limit=None):
        if limit is None:
            limit = self.max_token
        truncated = []
        # print("PromptSection Truncate (총 %d개) %d -> %d"% (len(self.prompt),self.token,limit))
        while True:
            if self.token <= limit:
                break
            if self.min_token is not None:
                if self.token <= self.min_token:
                    #print("min_break")
                    break
            removed = self.prompt.pop(0)
            #print("removed : %s" % removed.content)
            truncated.append(removed)
            #print(truncated)

        if len(truncated) > 0:
            logging.debug("PromptSection %s 에서 오래된 항목 %d개 제거" % (self.section, len(truncated)))
        return PromptSection(section="truncated", prompt=truncated)

    def append(self, prompt: Prompt, auto_truncate: bool = True):
        self.prompt.append(prompt)

        if auto_truncate:
            if self.max_token is not None:
                self.truncate(self.max_token)

    def toJSON(self):
        return str(self)

    def toList(self):
        return json.loads(str(self))

    def toPromptList(self):
        arr = []
        for p in self.prompt:
            arr.append(p)
        return arr


    def __str__(self):
        arr = []
        for p in self.prompt:
            arr.append({'role': p.role, 'content': p.content})

        return json.dumps(arr, sort_keys=True, ensure_ascii=False, indent=4)


class GPTPrompt:
    def __init__(self):
        self.section_list = []

        self.prompt_important_order = ['character_system', 'few_shot_assistant', 'summary_system', 'dialogue',
                                       'pre_user_text_system', 'user_text', 'post_user_text_system']

    def put(self, section: PromptSection):
        self.section_list.append(section)

    @property
    def token(self):
        token = 0
        for section in self.section_list:
            token = token + section.token
        return token

    def truncate(self, token_limit):
        while True:
            if self.token <= token_limit:
                break

            have_to_reduce_token = self.token - token_limit
            logging.info("GPTPrompt Truncation : have to reduce %d tokens" % have_to_reduce_token)

            for to_truncate_section in self.prompt_important_order.reverse():
                prompt_section = None
                for prompt_section in self.section_list:
                    if prompt_section.section == to_truncate_section:
                        break
                if prompt_section is not None:
                    prompt_section = self.prompt_section_dic[to_truncate_section]
                    prompt_section.truncate(limit=prompt_section.token - have_to_reduce_token)

    def __str__(self):
        # print("SECTION_LIST")

        final_list = []
        for section in self.section_list:

            # print(section.section)
            # print(len(section.prompt))
            # print(id(section.prompt))

            for p in section.prompt:
                final_list.append({'role': p.role, 'content': p.content})

        return json.dumps(final_list, sort_keys=True, ensure_ascii=False, indent=4)

