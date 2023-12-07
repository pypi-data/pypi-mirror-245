# Databricks Generative AI Inference SDK (Beta)

The Databricks Generative AI Inference Python library provides a user-friendly python interface to use the Databricks [Foundation Model API](https://docs.databricks.com/en/machine-learning/foundation-models/api-reference.html). 

It includes a pre-defined set of API classes `Embedding`, `Completion`, `ChatCompletion` with convenient functions to make API request, and to parse contents from raw json response. 

We also offer a high level `ChatSession` object for easy management of multi-round chat completions, which is especially useful for your next chatbot development.

You can find more usage details in our [SDK onboarding doc](https://docs.databricks.com/en/machine-learning/foundation-models/query-foundation-model-apis.html).

> [!IMPORTANT]  
> We're preparing to release version 1.0 of the Databricks GenerativeAI Inference Python library.

## Installation

```sh
pip install databricks-genai-inference
```

## Usage

### Embedding

```python
from databricks_genai_inference import Embedding
```

#### Text embedding

```python
response = Embedding.create(
    model="bge-large-en", 
    input="3D ActionSLAM: wearable person tracking in multi-floor environments")
print(f'embeddings: {response.embeddings[0]}')
```

#### Text embedding with instruction

```python
response = Embedding.create(
    model="bge-large-en", 
    instruction="Represent this sentence for searching relevant passages:", 
    input="3D ActionSLAM: wearable person tracking in multi-floor environments")
print(f'embeddings: {response.embeddings[0]}')
```

#### Text embedding (batching)

> [!IMPORTANT]  
> Support max batch size of 16

```python
response = Embedding.create(
    model="bge-large-en", 
    input=[
        "3D ActionSLAM: wearable person tracking in multi-floor environments",
        "3D ActionSLAM: wearable person tracking in multi-floor environments"])
print(f'response.embeddings[0]: {response.embeddings[0]}\n')
print(f'response.embeddings[1]: {response.embeddings[1]}')
```

#### Text embedding with instruction (batching)

> [!IMPORTANT]  
> Support one instruction per batch 
> Batch size

```python
response = Embedding.create(
    model="bge-large-en", 
    instruction="Represent this sentence for searching relevant passages:",
    input=[
        "3D ActionSLAM: wearable person tracking in multi-floor environments",
        "3D ActionSLAM: wearable person tracking in multi-floor environments"])
print(f'response.embeddings[0]: {response.embeddings[0]}\n')
print(f'response.embeddings[1]: {response.embeddings[1]}')
```

### Text completion

```python
from databricks_genai_inference import Completion
```

#### Text completion

```python
response = Completion.create(
    model="mpt-7b-instruct", 
    prompt="Represent the Science title:")
print(f'response.text:{response.text:}')

```

#### Text completion (streaming)

> [!IMPORTANT]  
> Only support batch size = 1 in streaming mode

```python
response = Completion.create(
    model="mpt-7b-instruct", 
    prompt="Count from 1 to 100:",
    stream=True)
print(f'response.text:')
for chunk in response:
    print(f'{chunk.text}', end="")
```

#### Text completion (batching)

> [!IMPORTANT]  
> Support max batch size of 16

```python
response = Completion.create(
    model="mpt-7b-instruct", 
    prompt=[
        "Represent the Science title:", 
        "Represent the Science title:"])
print(f'response.text[0]:{response.text[0]}')
print(f'response.text[1]:{response.text[1]}')
```

### Chat completion

```python
from databricks_genai_inference import ChatCompletion
```

> [!IMPORTANT]  
> Batching is not supported for `ChatCompletion`

#### Chat completion

```python
response = ChatCompletion.create(model="llama-2-70b-chat", messages=[{"role": "system", "content": "You are a helpful assistant."},{"role": "user", "content": "Knock knock."}])
print(f'response.text:{response.message:}')
```

#### Chat completion (streaming)

```python
response = ChatCompletion.create(model="llama-2-70b-chat", messages=[{"role": "system", "content": "You are a helpful assistant."},{"role": "user", "content": "Count from 1 to 30, add one emoji after each number"}], stream=True)
for chunk in response:
    print(f'{chunk.message}', end="")
```

### Chat session

```python
from databricks_genai_inference import ChatSession
```

> [!IMPORTANT]  
> Streaming mode is not supported for `ChatSession`

```python
chat = ChatSession(model="llama-2-70b-chat")
chat.reply("Kock, kock!")
print(f'chat.last: {chat.last}')
chat.reply("Take a guess!")
print(f'chat.last: {chat.last}')

print(f'chat.history: {chat.history}')
print(f'chat.count: {chat.count}')
```
