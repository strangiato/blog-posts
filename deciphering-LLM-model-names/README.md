# Deciphering LLM Model Names

One of the first challenges in working with Large Language Models (LLMs) is understanding their names.

This article hopes to help demystify some of the common naming conventions used by popular models.

## Branded Names

Unsurprisingly, models have names that help to brand them.  These names are intended to help identify a group of models that are produced by the same company and likely share some common architectures and training data.  Like any product name, its origin varies based on the model's creators and their intended branding message—whether technical, symbolic, or purely for marketing appeal.

IBM's Granite model evokes 'rock-solid' reliability, as its name suggests.

Alternatively, some names are derived from acronyms, like Meta's Llama which stands for **L**arge **La**nguage **M**odel **M**eta **A**I.  I'm sure the ability to create a fluffy mascot to go with name didn't hurt.

Data scientists have long used creative acronyms, dating back to early LLMs, such as ELMo (Embeddings from Language Models) and BERT (Bidirectional Encoder Representations from Transformers) which sparked a trend of Sesame Street inspired LLM names.

## Versions

Along with the branded name, models generally also include a version number.  Most models use a simplified semantic versioning system with Major and Minor version numbers, often omitting patch versions.

Major version number changes generally indicate a major change, such as an update to the underlying model architecture or training technique, updates to the training data, or perhaps even a significant change to the model performance.

A major version change may indicate compatibility issues with LLM-serving tools like vLLM, potentially requiring new releases to support the new model version.

Minor version number changes generally correspond to incremental improvements to the model or a retraining on updated data.

## Model Size

Most models will include some number in the model name such as "8B" or "278M" indicating parameter count in billions (B) or millions (M).  Parameters (or weights) are numerical values learned during training, used in the model's calculations when generating responses.

The number of parameters directly impacts the size of the model when it is stored as a file, and how much vRAM is needed to load the model onto a GPU.

For example, a Granite 8B model can reasonably fit on an NVIDIA A10 GPU with 24 GB of vRAM, while a Llama 405B model requires over 900 GB of vRAM and is commonly run on sixteen H100's with 80 GB of vRAM each.

## Model Purpose

LLMs are designed for different tasks, and understanding their use cases is crucial in selecting the right model. The purpose of the model is often included directly in the name of the specific model.

### Base Models

Base models are the "generic" model that act as the starting point for other more specialized models.  These models are rarely used "out of the box" and typically serve as a foundation for fine-tuning a model for specific purposes.

Some companies include "base" in the model name to make it explicit that the model is intended for fine-tuning, but others do not.

### Instruct

Instruct models are one of the most common model types you will encounter, and if you are looking for a conversational model this is most likely what you want.

Instruct models are fine tuned to be instructed what to do and are ideal for prompt engineering and general chat use cases.

Some older models will use "chat" to describe the model but that has fallen out of favor for "instruct" in most modern models.

### Vision

Vision models are an emerging category of models that are becoming rapidly adopted.  Vision models are generally multi-modal, meaning that they can accept both text and images as an input and provide text as an output.

Vision models can be useful for asking questions about an image, asking the model to describe the content of an image, or even doing image-to-text conversion.

Some models are labeled as `vision-instruct` models meaning that they are optimized to do both and can be a good choice if you are looking for a general chat model, that can also do vision tasks.

### Code

Code models are optimized to help with coding activities and coding assistants.

Dedicated code models have fallen out of favor compared to general instruct models and many newer instruct models will include the ability to act as a code model as well.

### Embedding

Embedding is the process of converting text to a numerical token that can be stored, queried, and retrieved from a vector database.  Embedding models are often used in RAG (Retrieval-Augmented Generation) alongside instruct models.

### Guard or Guardian Models

Guard or Guardian models are designed to help identify unsafe content or questions.  Different guard models will validate for different criteria but in general are looking for things that an AI Engineer/Developer would not want the instruct model to respond to.  For example, granite-guardian-3.2-5b checks for the following categories:

* Social Bias
* Jailbreaking
* Violence
* Profanity
* Sexual Content
* Unethical Behavior
* Harm Engagement
* Evasiveness

Guard models are often used in chat based workflows where the users question is first sent to the Guard model which attempts to determine if it is safe to proceed, and then the question is sent to the instruct model.  Sometimes the Guard model may also be used on the response from the LLM as well to ensure that the model is not responding with unacceptable content.

In the case that a Guard model does detect un-allowed language it will often respond a simple pre-determined response stating that it can't respond to that type of question.

### Reasoning Models

DeepSeek R1 recently put reasoning models on the map for the general public as it took the world and stock market by storm.

Unlike traditional LLMs that simply attempt to predict the next word in the sequence, reasoning models try to work through a "chain-of-thought" processing—internally asking and refining questions before delivering a final response.

## Quantization

Model names may include terms like "fp8", "int8", or "w4a16" indicating precision levels used for storage and performance.

These numbers refer to the data types the model has been published using.

Generally models are trained using either 32-bit or 16-bit floating point numbers and are converted to lower precision types such as 8-bit floating point or integer values that require less space to store and load into vRAM.  The process of converting models to the lower precision data types is called quantization.

The quantization of models can have significant impacts on the size of the model.  The Llama 405b model discussed earlier that requires 900+ GB uses a fp16 data type, but converting that to fp8 drops the model to around 450 GB.

The process of quantizing a model can decrease the accuracy and quality of responses but ideally that drop in quality is negligible.

Some Neural Magic models will also use a naming convention such as "w4a16" which indicates that the weight parameters use 4-bit values while the activation parameters retain the original 16-bit data types.  Using advanced quantization techniques Neural Magic is able to optimize the models for different scenarios with minimal impact to accuracy and performance.

To learn more about how Neural Magic applies these techniques to Granite models, take a look at their [blog](https://neuralmagic.com/blog/introducing-compressed-granite-3-1-powerful-performance-in-a-small-package/).

## Distillation

Distillation, a technique for creating smaller, more efficient models from larger ones, has recently gained traction—most notably with DeepSeek.

In simple terms, distillation is a technique where data scientists attempt to create a new, smaller model (a student model) using an existing larger model (the teacher model).  This technique attempts to reduce the training time and produce models that are smaller and faster than their teacher models while maintaining similar accuracy and response quality.

With models such as [deepseek-r1-distill-llama-70b](https://huggingface.co/deepseek-ai/DeepSeek-R1-Distill-Llama-70B) we can infer that this version of the model was trained using Llama 70B as the teacher model.

## Final Thoughts

Understanding LLM model names may seem overwhelming at first, but once you understand some key naming components it becomes much easier to navigate.

As the field continues to evolve, new naming conventions will continue to emerge, but with this guide, you now have a solid foundation to navigate LLM model names with confidence.
