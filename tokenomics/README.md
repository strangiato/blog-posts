# The Tokenomics of Self-Hosted LLMs

In the world of foundation models from providers like OpenAI or Anthropic, understanding the cost of a model starts as a simple price per million tokens.

However, once you step into the world of self-hosting your own models, that "price" is not as easy to understand.  *Tokenomics* (the economics of how tokens are produced and what they effectively cost) requires looking at both what you spend and how much you serve.

In this article we will walk through a practical way to calculate cost per token for self-hosted LLMs, and the levers that move that number: spend less, and serve more.

## A Simple Formula

At its core, cost per token is:

**Cost per token = operating cost ÷ tokens processed**

Over the same period of time.  For example, a single month.  To improve that metric, you can reduce the overall cost, increase the number of tokens processed, or both.

Here is a worked example we will return to throughout this article.  Suppose your LLM infrastructure costs about **$50,000 per month** and you process **500 million tokens** in that month:

**$50,000 ÷ 500M tokens ≈ $0.10 per million tokens**

If you cut monthly cost to $40,000 without changing usage, cost per million tokens drops to about $0.08.  If instead you keep the $50,000 spend but grow usage to 1,000M tokens, cost per million tokens drops to about $0.05.  Both paths improve the metric.

## Cost

Cost can be broken down into a few high-level categories:

* Hardware/Infrastructure
* Software
* People
* Other

When you are operating in a cloud model, Hardware/Infrastructure costs are generally the most straightforward since these end up on a monthly bill from your cloud provider.  At the end of the day you are paying a specific rate per hour for the instance type you have deployed, along with additional costs related to network traffic and storage.

However, if you are self-hosting your own hardware, things can get a little more complicated.  Let's say that you purchased a node for $500k as a capital expenditure.  In order to understand the cost of that node for a single month, you would need to understand the expected lifespan of that node and depreciate the cost of it over that period of time.  In simpler terms, if you expect to use that node for four years, you can take $500k/48 to get a monthly cost of about **$10,400**.  In addition to the nodes themselves, you probably also need to factor in other hardware such as networking hardware.

For both scenarios, you may also want to factor in the cost of other hardware in the cluster, such as your control planes.  If you are running your GPU workloads in a multi-tenant environment with other use cases, you may wish to spread these costs across all of your use cases.

Software is another area to factor in.  If you are using OpenShift AI, the most common SKU purchased by customers is OpenShift AI Enterprise, which includes entitlements for OpenShift, OpenShift AI, and accelerators on that node.  While some customers may choose to pay for the individual pieces of software separately, these are the main software costs from Red Hat.

The cost of the people needed to deploy, support, and manage your LLM infrastructure is an often overlooked aspect of running your own LLMs.  Often, organizations have a dedicated team that manages multiple OpenShift clusters, and a portion of that team's time could be allocated and tracked toward the cost of running your own LLMs.  In addition, organizations will often have a separate team that is responsible for the models themselves.  Platform tooling can reduce that burden.  For example, it can make it easier to source models and keep a supported vLLM runtime current, but people remain part of the true operating cost.

Finally, "other" costs are a catch-all for "how deep do you want to go?"  For most high-level calculations the items above are sufficient, but if you want a fuller total cost of ownership you could consider power consumption, cooling, data center support personnel, or even the real estate the server rack sits on.

### Optimizing Costs

Now that we have a baseline understanding of the cost categories, we can start thinking about how we can reduce the cost side of the formula, and therefore the $50,000 in our example.

For infrastructure costs, the biggest opportunity generally comes from right-sizing your deployments.  If you are deploying a smaller model with fairly low, sporadic usage, you may not need a `p5.48xlarge` with eight H100s and can instead opt for a more budget-friendly `g6e.48xlarge` with eight L40S GPUs.

Autoscaling both the model server replicas and the nodes in the cloud environment can also have a dramatic impact on the cost of running an LLM.  Letting instances scale down to a minimum number of replicas while usage is low, and automatically scaling them back up when traffic is heavier, is a strong way to reduce overall cost while still maintaining required Service Level Objectives (SLOs).

For self-hosted environments, you can still take advantage of autoscaling to reduce how much hardware a specific model is using and free up those resources for other use cases, such as overnight batch training jobs, to spread the cost of the hardware across multiple workloads.  Additionally, while you are committed to the hardware you have purchased, spending more time up front to understand what models you plan to deploy, and how many requests/tokens you need to serve, can help you right-size before making hardware purchases.

Software choices also affect people cost.  Platforms like OpenShift AI make it easier to source models and run supported vLLM releases from a container registry, which reduces the time teams spend building and maintaining custom inference images, and that time is part of your operating cost.

## Tokens Processed

Tokens processed can be evaluated from two different lenses: your **theoretical maximum** (how many tokens the system *could* process) and your **actual tokens processed** (how many you *did* process over a period of time).

You can derive the theoretical maximum by performing load testing with tools such as [GuideLLM](https://github.com/vllm-project/guidellm), which simulates realistic workloads and ramps concurrent connections until performance starts to degrade.  Based on that result, you can estimate the theoretical maximum number of tokens you can process in a period of time.  For example, if you were able to process 1M tokens per minute you could theoretically process 1,440M tokens per day.

In most scenarios you will not be able to sustain that level of maximum load 24/7. However, theoretical maximum is still useful for right-sizing and capacity planning.  For example, deciding how many replicas you need to meet real-world demand.  If you have built a system that can process 1,440M tokens per day, but you are only processing 50M, you may be over-provisioned relative to demand, which keeps the cost side of the formula high relative to the tokens side.

Measuring real-world token processing is the better metric for deriving cost per token.  Returning to our example: $50,000 ÷ 500M tokens is your true cost per token for that month, not $50,000 divided by the theoretical maximum you could have served if the system ran flat-out.

### Optimizing Tokens Processed

The biggest impact on cost per token usually comes from **increasing overall usage**, not from squeezing more peak throughput out of an underutilized system.  If your system can process 1,440M tokens per day but you are only processing 500M, driving more use cases onto the platform, or growing usage of existing ones, improves the denominator directly.  In our monthly example, growing from 500M to 1,000M tokens at the same $50,000 spend halves cost per million tokens.

It also helps to better utilize the system in non-peak hours.  Shifting batch workloads to off hours can raise tokens processed without adding hardware, while keeping performance high for peak interactive traffic.

Teams often turn next to **optimizing the model deployment** itself by tuning serving configuration, batching, and related settings to raise throughput.  That work primarily increases theoretical maximum capacity, not actual tokens processed.  If you optimize a deployment from 1,440M to 1,800M tokens per day of capacity (+25%) but real-world usage stays at 500M, cost per token does not move.

Those optimizations still matter as *enablers*: higher capacity can absorb additional use cases without new hardware, or let you scale down to fewer resources if demand is already met.  Treat them as a way to either grow the tokens side or shrink the cost side, not as an automatic win on cost per token by themselves.

## The Impact of Model Choice

The model you choose pulls on both sides of the formula.  Larger models usually raise the cost side through more GPUs per replica.  They may also change how many tokens you can serve per dollar on the tokens side through throughput and latency characteristics.

A model such as [Llama-3.1-8B-Instruct](https://huggingface.co/meta-llama/Llama-3.1-8B-Instruct) is significantly smaller than [Llama-3.3-70B-Instruct](https://huggingface.co/meta-llama/Llama-3.3-70B-Instruct).  The 8B model can easily fit on a single H100, or a more budget GPU like an L40S, while the 70B model may require up to four H100s to serve a single instance.  Choosing the smaller model when quality is "good enough" for the use case can cut hardware cost sharply, while also enabling higher total throughput and if that frees budget or capacity for more traffic, cost per token improves further.

Quantization is another lever.  An fp8 (8-bit floating point) version of the 70B model could be deployed on two H100s instead of four, reducing hardware required while aiming to preserve much of the model's quality.  Quantized or smaller models may also sustain higher tokens per second, which only improves cost per token if you use that extra capacity or scale the deployment down.

## Input Tokens, Cached Tokens, and Output Tokens

When dealing with cloud providers, you will often see different prices depending on the type of tokens being processed.  Even when you self-host, those same token types still have different *effective* costs, because they consume the GPU differently.  Your mix of input, cached, and output tokens therefore shapes real cost per token, even when you are not paying a published per-token rate.

**Input tokens** are generally processed in a single pass.  Model servers like vLLM can take strong advantage of continuous batching here, so input-heavy workloads are often highly parallelized and relatively efficient per token.

**Cached tokens** are tokens that have already been computed and are available in the GPU's KV cache (the key-value cache vLLM uses to avoid recomputing attention state for repeated context).  vLLM can reuse cached tokens when queries share common system prompts, or in multi-turn conversations where chat history is resent with each request.  Cached tokens are generally very cheap because the value is looked up rather than recomputed on the GPU.

Projects like [llm-d](https://github.com/llm-d/llm-d) can increase the chance of a KV cache hit in multi-replica deployments through intelligent routing that sends related requests to replicas more likely to already hold the relevant cache, which improves total throughput and possibly reduce the effective cost when your traffic has shared context.

**Output tokens** are highly iterative: each token is predicted one at a time.  That process generally makes output tokens more expensive in GPU time than input or cached tokens, so output-heavy workloads push effective cost per token higher for the same headline token count.

Speculative decoding is one option that can improve the efficiency of output tokens.  With speculative decoding, a smaller draft model predicts several tokens ahead, and the larger model verifies those predictions.  Accepted tokens are kept, and rejected ones are regenerated.  The result is faster output generation with the same final text, raising useful tokens served per unit of GPU time when verification succeeds often enough.

## Final Thoughts

Self-hosted LLM pricing is less about a sticker price per million tokens and more about understanding what you spend and how much you actually serve.  Cost per token is operating cost (hardware, software, people, and whatever else you include) divided by tokens processed over the same period.  You improve that number by cutting spend through right-sizing and autoscaling, by increasing real-world utilization so idle capacity is put to work, or by choosing models and serving techniques that better match your workload.

The most useful takeaway is to measure both sides of the equation.  Track actual tokens processed, not just theoretical maximum throughput, and account for how input, cached, and output tokens behave differently under vLLM.  With that visibility, model choice, quantization, speculative decoding, and routing for cache hits become deliberate levers rather than guesswork, and you can compare self-hosted economics against managed APIs on equal footing.
