"""Basic Extractor that is purely example driven."""
import json
import logging
import re
from copy import copy
from dataclasses import dataclass
from typing import List
import openai, tiktoken
from openai import OpenAI

from ..utils.tokens import estimate_num_tokens, max_tokens_by_model
from .extractor import AnnotatedObject, Extractor

logging.basicConfig(filename='custom_allmodels.log', filemode='a')
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


@dataclass
class BasicExtractor(Extractor):

    """
    Extractor that is purely example driven.
    """

    serialization_format: str = "json"
    model_name: str = "gpt-3.5-turbo"
    client = OpenAI()


    def get_task_description(self, target_class, query_term):
        return f"""
        You must follow the steps below for a correct answer. Otherwise your answer will be considered invalid.
        1) Extract a {target_class} object from text in {self.serialization_format} format using the 'Background' section above only as a reference of how the '{query_term}' term is connected with other terms.
        2) Analyze the examples below and try to connect the query term '{query_term}' with the terms in the examples if they logically should and can be connected.
        3) Ensure that no relationships or concepts are hallucinated. When generating relationships for the term '{query_term}', every relationship and concept used must be strictly derived from the given examples below.
        4) Do not create any relationships or introduce any concepts that are not explicitly present in the provided examples.
        5) Additionally, the generated response must only adhere to the format of the examples given below.
        6) The generated properties of the {target_class} must have values inspired only from the example below.
        7) Always have the '{query_term}' as the 'prefLabel' generated property \n\n
    """


    def count_tokens(self, text, model_name='gpt-3.5-turbo-instruct'):
        tokenizer = tiktoken.encoding_for_model(model_name)
        tokens = tokenizer.encode(text)
        return len(tokens)


    # def openaimodel(self, prompt):
    #     """This code works for when we don't have much context!"""
        
    #     print('Running turbo instruct model')
    #     max_context_length = 4097
    #     conservative_max_tokens = 1000  # Initial conservative max tokens for response

    #     # Count tokens for the input prompt
    #     prompt_token_count = self.count_tokens(prompt)

    #     if prompt_token_count >= max_context_length:
    #         raise ValueError("Prompt is too long to fit within the model's context length")

    #     # # Make an initial API call with a conservative max_tokens value
    #     initial_response = self.client.completions.create(
    #         prompt=prompt,
    #         model='gpt-3.5-turbo-instruct',
    #         max_tokens=conservative_max_tokens
    #     )

    #     initial_response_text = initial_response.choices[0].text
    #     # print(f'The response is: {initial_response_text}')
    #     initial_response_token_count = self.count_tokens(initial_response_text)

    #     # Calculate remaining tokens available for the response
    #     remaining_tokens = max_context_length - prompt_token_count - initial_response_token_count

    #     # Adjust max_tokens for the final response if necessary
    #     final_max_tokens = min(remaining_tokens, conservative_max_tokens)

    #     if final_max_tokens <= 0:
    #         raise ValueError("Prompt and initial response are too long to fit any further response within the model's context length")

    #     # If the initial response is sufficient, return it
    #     if initial_response.choices[0].finish_reason == "stop":
    #         return initial_response

    #     # Otherwise, make a follow-up call with the adjusted max_tokens
    #     final_response = self.client.completions.create(
    #         prompt=prompt,
    #         model='gpt-3.5-turbo-instruct',
    #         max_tokens=final_max_tokens
    #     )

    #     print(final_response)
    #     return final_response



    #New code for more context!! (Trimming some background context)
    def openaimodel(self, prompt):
        print('Running turbo instruct model')
        max_context_length = 4097
        conservative_max_tokens = 1000  # Initial conservative max tokens for response
        trim_amount = 50  # Number of tokens to trim if the context is too long

        def get_truncated_background(prompt, trim_amount):
            print("Need to trim prompt!!!")
            # Split prompt into parts using the delimiter '---'
            parts = prompt.split('---')
            if len(parts) < 2:
                raise ValueError("Prompt format is incorrect. Expected '---' delimiter.")
            background, examples = parts[0], '---' + parts[1]
            # Tokenize the background section
            background_tokens = background.split()
            # Trim the background section by the specified number of tokens
            truncated_background = ' '.join(background_tokens[:-trim_amount])
            # Reconstruct the prompt with the truncated background
            return truncated_background + examples

        def count_tokens(text):
            # Token counting function placeholder, replace with actual implementation
            return len(text.split())

        # Count tokens for the input prompt
        prompt_token_count = count_tokens(prompt)

        while True:
            try:
                # Calculate initial max tokens based on the truncated prompt length
                initial_max_tokens = max_context_length - prompt_token_count

                # Make an initial API call with the initial max_tokens value
                initial_response = self.client.completions.create(
                    prompt=prompt,
                    model='gpt-3.5-turbo-instruct',
                    max_tokens=min(conservative_max_tokens, initial_max_tokens)
                )

                initial_response_text = initial_response.choices[0].text
                initial_response_token_count = count_tokens(initial_response_text)

                # Calculate remaining tokens available for the response
                remaining_tokens = max_context_length - prompt_token_count - initial_response_token_count

                if remaining_tokens <= 0:
                    raise ValueError("Prompt and initial response are too long to fit any further response within the model's context length")

                # If the initial response is sufficient, return it
                if initial_response.choices[0].finish_reason == "stop":
                    return initial_response

                # Otherwise, make a follow-up call with the adjusted max_tokens
                final_response = self.client.completions.create(
                    prompt=prompt,
                    model='gpt-3.5-turbo-instruct',
                    max_tokens=min(remaining_tokens, conservative_max_tokens)
                )

                print(final_response)
                return final_response

            except Exception as e:
                print(f"Error encountered: {e}")
                prompt = get_truncated_background(prompt, trim_amount)
                prompt_token_count = count_tokens(prompt)
                print(f"Trimming prompt. New prompt length: {prompt_token_count} tokens")


    def extract(
        self,
        text: str,
        target_class: str,
        examples: List[AnnotatedObject] = None,
        background_text: str = None,
        rules: List[str] = None,
        min_examples=1,
        **kwargs,
    ) -> AnnotatedObject:
        
        logger.debug(f"Basic extractor: {text}, {len(examples)} examples")
        examples = copy(examples)
        while True:
            prompt = ""
            if background_text:
                prompt += f"{background_text}\n\n"
            query_term = text.split(":")[-1].strip()
            prompt += self.get_task_description(target_class, query_term) 
            # prompt += f"Extract a {target_class} object from text in {self.serialization_format} format.\n\n"
            if rules:
                prompt += "Rules:\n\n"
                for rule in rules:
                    prompt += f"- {rule}\n"
                prompt += "\n"
                prompt += "---\n"
            prompt += "Examples:\n\n"
            for example in examples:
                if example.text:
                    prompt += f"##\nText: {example.text}\n"
                prompt += f"Response: {self.serialize(example)}\n"
            prompt += f"\n##\nText: {text}\n\n"
            prompt += "Response: "
            estimated_length = estimate_num_tokens([prompt])
            if estimated_length + 300 < max_tokens_by_model(self.model.model_id):
                break
            else:
                # remove least relevant
                logger.debug(f"Removing least relevant of {len(examples)}: {examples[-1]}")
                examples.pop()
                if len(examples) < min_examples:
                    raise ValueError(
                        f"Prompt too long, need at least {min_examples} examples: {prompt}."
                    )
        model = self.model
        
        logger.info(f"Prompt: {prompt}")
        if 'instruct' in str(model):
            response = self.openaimodel(prompt)
            ao = self.parse_openai_response(response)
            # print(ao)
        else:
            print(type(model))
            response = model.prompt(prompt, temperature=0.8)
            ao = self.deserialize(response.text())
        ao.annotations["prompt"] = prompt
        return ao


    def serialize(self, ao: AnnotatedObject) -> str:
        return json.dumps(ao.object)


    def deserialize(self, text: str) -> AnnotatedObject:
        logger.debug(f"Parsing {text}")
        try:
            obj = json.loads(text)
            if isinstance(obj, str):
                if self.raise_error_if_unparsable:
                    raise ValueError(f"Could not parse {text}")
                else:
                    obj = {}
            return AnnotatedObject(object=obj)
        except Exception as e:
            match = re.search(r"\{.*\}", text)
            if match:
                if match.group() != text:
                    return self.deserialize(match.group())
            if self.raise_error_if_unparsable:
                raise e
            else:
                logger.warning(f"Could not parse {text}")
                return AnnotatedObject(object={})



    def parse_openai_response(self, response: dict) -> AnnotatedObject:
        """
        Parses the OpenAI API response and deserializes the text in the choices field.
        
        :param response: The OpenAI API response
        :return: AnnotatedObject
        """
        print(response.choices[0].text)
        print('choices' in response )
        logger.debug(f"Received response: {response}")
        if response.choices[0].text is not None:
        # if 'choices' in response and len(response['choices']) > 0:
            # text = response['choices'][0].get('text', '')
            text = response.choices[0].text
            logger.debug(f"Text to deserialize: {text}")
            return self.deserialize(text)
        else:
            logger.warning("No choices found in the response or choices are empty.")
            return AnnotatedObject(object={})
