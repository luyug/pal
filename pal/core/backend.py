# Copyright 2022 PAL Authors. All rights reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import openai
import time
import os

openai.api_key = os.getenv('OPENAI_API_KEY')

# GPT-3 API
def call_gpt(prompt, model='code-davinci-002', stop=None, max_tokens=128, temperature=0., majority_at=None):
    for i in range(20):
        try:
            best_of = num_completions = majority_at if majority_at is not None else 1
            ans = openai.Completion.create(
                            model=model,
                            max_tokens=max_tokens,
                            stop=stop,
                            prompt=prompt,
                            temperature=temperature,
                            n=num_completions,
                            best_of=best_of)
            return [choice['text'] for choice in ans['choices']]
        except openai.error.RateLimitError as e:
            time.sleep(min(2**i, 60))
    raise RuntimeError('Failed to call GPT API')
