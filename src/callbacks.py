import time
import random
from langchain.callbacks.base import BaseCallbackHandler

class StreamHandler(BaseCallbackHandler):
    def __init__(self,container,initial_text=""):
        self.container = container
        self.text = "Generated text :  \n"

    def on_llm_new_token(self,token,**kwargs):
        for letter in token:
            delay = random.uniform(0.0005,0.001)
            time.sleep(delay)
            self.text += letter
            self.container.markdown(self.text)