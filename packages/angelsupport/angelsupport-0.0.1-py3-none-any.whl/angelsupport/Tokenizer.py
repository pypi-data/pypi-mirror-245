import tiktoken

class Tokenizer:

    @classmethod
    def encoder(cls, backend):
        try:
            encoder = tiktoken.encoding_for_model(backend)
        except KeyError:
            print("Warning: model not found. Using cl100k_base encoding.")
            encoder = tiktoken.get_encoding("cl100k_base")
        if backend in {
            "gpt-3.5-turbo-0613",
            "gpt-3.5-turbo-16k-0613",
            "gpt-4-0314",
            "gpt-4-32k-0314",
            "gpt-4-0613",
            "gpt-4-32k-0613",
        }:
            tokens_per_message = 3
            tokens_per_name = 1
        elif backend == "gpt-3.5-turbo-0301":
            tokens_per_message = 4  # every message follows <|start|>{role/name}\n{content}<|end|>\n
            tokens_per_name = -1  # if there's a name, the role is omitted
        elif "gpt-3.5-turbo" in backend:
            print("Warning: gpt-3.5-turbo may update over time. Returning num tokens assuming gpt-3.5-turbo-0613.")
            return cls.encoder(backend="gpt-3.5-turbo-0613")
        elif "gpt-4" in backend:
            print("Warning: gpt-4 may update over time. Returning num tokens assuming gpt-4-0613.")
            return cls.encoder(backend="gpt-4-0613")
        else:
            raise NotImplementedError(
                f"""num_tokens_from_messages() is not implemented for model {backend}. See https://github.com/openai/openai-python/blob/main/chatml.md for information on how messages are converted to tokens."""
            )
        return encoder, tokens_per_message, tokens_per_name


    @classmethod
    def num_tokens_from_messages(cls, messages, backend="gpt-3.5-turbo-0613"):

        if type(messages) is dict:
            messages = [messages]

        """Return the number of tokens used by a list of messages."""
        encoder, tokens_per_message, tokens_per_name = cls.encoder(backend)

        num_tokens = 0
        for message in messages:
            num_tokens += tokens_per_message
            for key, value in message.items():
                num_tokens += len(encoder.encode(value))
                if key == "name":
                    num_tokens += tokens_per_name
        num_tokens += 3  # every reply is primed with <|start|>assistant<|message|>
        return num_tokens
