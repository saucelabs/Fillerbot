from .generator import Generator
import json
import requests
from faker import Faker
from transformers import pipeline


class LanguageModelGenerator(Generator):
    def __init__(self, name, desc=None, gen_id=None, var_name=None, data_item=None, create_date=None, n_items=1):
        super(LanguageModelGenerator, self).__init__(name, desc, gen_id, var_name, create_date)
        self.model = data_item['model']
        self.prompt = data_item['prompt']
        self.temperature = float(data_item["temperature"]) if "temperature" in data_item else 1.0
        self.max_tokens = data_item['max_tokens'] if "max_tokens" in data_item else None
        self.n_items = n_items

        self.faker = Faker()
        self.data_bank = None
        self.index = 0

    # Preprocess the prompt to allow Faker and context Injections
    def pre_process_prompt(self, context=None):
        new_context = context
        initial_prompt = self.prompt
        post_processed_prompt = ""
        splits = initial_prompt.split(" ")
        # Now here we replace it and be done with it
        for split in splits:
            if "faker" in split:
                subst = split.split(".")
                try:
                    method = getattr(self.faker, subst[1])
                except AttributeError:
                    raise NotImplementedError(
                        "Class `{}` does not implement `{}`".format(self.faker.__class__.__name__, subst[1]))
                post_processed_prompt += str(method()) + " "
            elif "globalcontext" in split:
                subst = split.split(".")
                try:
                    contextvar = new_context[subst[1]]
                    print("contextvar" + str(contextvar))
                except AttributeError:
                    raise NotImplementedError("Context Name `{}` does not exist".format(subst[1]))
                post_processed_prompt += contextvar + " "
            else:
                post_processed_prompt += split + " "
        print(post_processed_prompt)
        return post_processed_prompt


class HFTextGenGenerator(LanguageModelGenerator):
    def __init__(self, name, desc=None, gen_id=None, var_name=None, data_item=None, create_date=None, n_items=1):
        super(HFTextGenGenerator, self).__init__(name, desc, gen_id, var_name, data_item, create_date, n_items)
        self.description = 'Hugging Face Text Generation Generator!'
        self.type_label = 'HFTextGenGenerator'
        self.do_sample = data_item["do_sample"] if "do_sample" in data_item else True
        self.top_k = int(data_item["top_k"]) if "top_k" in data_item else None
        self.top_p = float(data_item["top_p"]) if "top_p" in data_item else None
        self.repetition_penalty = float(data_item["repetition_penalty"]) if "repetition_penalty" in data_item else None
        self.max_new_tokens = data_item["max_new_tokens"] if "max_new_tokens" in data_item else None
        self.return_full_text = data_item["return_full_text"] if "return_full_text" in data_item else True

        self.generator = pipeline('text-generation', model=self.model)

    def generate(self, context=None):
        new_context = context
        new_prompt = self.pre_process_prompt(new_context)
        if self.data_bank is None:
            self.data_bank = self.generator(new_prompt, do_sample=self.do_sample, max_length=self.max_tokens,
                                            num_return_sequences=self.n_items, temperature=self.temperature,
                                            top_k=self.top_k, top_p=self.top_p, max_new_tokens=self.max_new_tokens,
                                            repetition_penalty=self.repetition_penalty,
                                            return_full_text=self.return_full_text)

        if self.index >= len(self.data_bank):
            self.index = 0

        instance = self.data_bank[self.index]['generated_text']
        self.index += 1
        return instance


class Jurassic1Generator(LanguageModelGenerator):
    def __init__(self, name, desc=None, gen_id=None, var_name=None, data_item=None, create_date=None, n_items=1):
        super(Jurassic1Generator, self).__init__(name, desc, gen_id, var_name, data_item, create_date, n_items)
        self.description = 'Jurassic 1 Generator!'
        self.type_label = 'Jurassic1Generator'
        #API Parameters
        self.apitoken = data_item['apitoken']
        self.stop_sequences = data_item['stop_sequences']
        self.topKReturn = data_item['topKReturn']
        self.index = 0

    #Use this one for batch requests
    def prepare_data_bank(self, new_prompt):
        payload = {
            "prompt": new_prompt,
            "numResults": self.n_items,
            "maxTokens": self.max_tokens,
            "stopSequences": self.stop_sequences,
            "topKReturn": self.topKReturn,
            "temperature": self.temperature
        }
        resp = requests.post(f"https://api.ai21.com/studio/v1/{self.model}/complete",
                             headers={"Authorization": f"Bearer {self.apitoken}"},
                             json=payload)
        data = json.loads(resp.text)
        data_bank = []
        for completion in data["completions"]:
            data_bank.append(completion["data"]["text"])
        return data_bank
         
    #Instead what we are going to do, is to make an option called context-sensitive
    #We will process the prompt either way, but if it's batched it goes batched.
    def generate(self, context=None):
        new_context = context
        new_prompt = self.pre_process_prompt(new_context)
        if self.data_bank is None:
            self.data_bank = self.prepare_data_bank(new_prompt)

        if self.index >= len(self.data_bank):
            self.index = 0

        instance = self.data_bank[self.index]
        self.index += 1
        return instance
