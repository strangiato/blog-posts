# The Tokenomics of Self Hosted LLMs

In the world of foundation models from providers like OpenAI or Anthropic, understanding the cost of a model starts as a simple price per million tokens.

However, once you step into the world of self hosting your own models, the "price" is not as easy to understand.

In this article we will explore how to derive the cost per token of running your own LLM and explore some of the factors that can impact that calculation.

To begin, we can define a simple formula of how much it costs to operate your LLMs divided by the total number of tokens you processed over a specific period of time.  In order to reduce the cost per token metric, you can either reduce the overall cost, or you can increase the number of tokens.

For the sake of this article we will be primarily focus on the cost for a single month of operations but 

## Cost

Cost can be broken down into a few high level categories:

* Hardware/Infrastructure
* Software
* People
* Other

When you are operating in a cloud model, Hardware/Infrastructure costs are generally the most straight forward since this is ends up on a monthly bill from your cloud provider.  At the end of the day you are likely pay a specific rate per hour for the instance type you have deployed along with other additional costs related to network traffic and storage that you are using in that instance.  At the time of writing this article, an `p5.48xlarge` instance type with eight H100's has an On Demand price of about $55 an hour, meaning that if you run that instance type for a month the approximate cost would be around $41k before any additional charges for networking or storage.

However, if you are self hosting your own hardware, things can get a little bit more complicated.  Let's say that you purchased an node for $500k as a capital expenditure.  In order to understand the cost of that node for a single month you would need to understand the expected lifespan of that node and depreciate the cost of it over that period of time.  In simpler terms, if you expect to use that node for four years, you can take the $500k/48 to get a monthly cost of $10,400 a month.  In addition to the nodes themselves, you probably also need to factor in other hardware such as networking hardware as well.

For both scenarios, you may also want to factor in the cost of other hardware in the cluster such as your control planes.  If you are running your GPU workloads in a multi-tenant environment with other use cases you may wish to spread these costs across all of your use cases.

Software are another area to factor in for costs.  If you are using OpenShift AI the most common SKU purchased by customers is OpenShift AI Enterprise, which includes entitlements for OpenShift, OpenShift AI, and any accelerators in that node.  While some customers may choose to pay for the individual pieces of software separately, these are the main software costs from Red Hat.

The cost of the people needed to deploy, support and manage your LLM infrastructure is an often overlooked aspect of running your own LLMs.  Often times organizations have a dedicate team that manage multiple OpenShift clusters and a portion of that teams time could be allocated and tracked towards the cost of running your own LLMs.  In addition, organizations will often have a separate team that is responsible for the models themselves.  OpenShift AI helps to cut down the time it takes to deploy and support models but it still takes people to manage these systems.

Finally, "other" costs are a catch all for "how far deep do you want to go?" with additional costs.  For most high level calculations the items above are sufficient, but if you want to understand the total cost you could consider things like power consumption, cooling costs, the cost of the support personnel needed to manage the data center, or even the cost of the real estate that the server rack sits on.  Any number of items can be added in to help get a true total cost of ownership estimation.

### Optimizing Costs

Now that we have a baseline understanding of the cost categories, we can start thinking about how we can reduce those costs.

For infrastructure costs, the biggest opportunity generally comes from right sizing your deployments.  If you are deploying a smaller model that will have fairly low, sporadic usage, you may reconsider needing `p5.48xlarge` with eight H100's and instead opt for a more budget `g6e.48xlarge` with eight L40s'.

Autoscaling both the model server replicas and the nodes in the cloud environment can also have a dramatic impact on the cost of running an LLM.  Letting instances scale down to a minimum number of replicas while usage is low and automatically scaling them back up when traffic is heavier is a fantastic way to reduce the overall cost while still maintaining required Service Level Objectives (SLOs).

For self hosted environments, we can still take advantage of things like Autoscaling to reduce how much hardware a specific model is using and free up those resources for other use cases such as running overnight batch training jobs to spread the cost of the hardware across multiple use cases.  Additionally, while you are committed to the hardware you have purchased, spending more time up front to understand what models you plan to deploy, and how many requests/tokens you need to serve can help you to better right size your deployment before making hardware purchases.

Software can also have a major impact on the people costs of running your own LLMs.  OpenShift AI helps to make it easier to source both models and software like vLLM securely and reliably.  Tools like OpenShift AI help to make managing your models easier and free those individuals up to work on other efforts.  OpenShift AI's model catalog help organizations source models from Red Hat's container registry, while Red Hat's regular vLLM releases help organizations to run the latest models without needing to navigate building their own vLLM containers.

## Tokens Processed

Token processed can be evaluated from two different lenses.  The first is by looking at your theoretical maximum number of tokens the system you have built can process, and the second is by looking at the actual tokens you have processed over a period of time.

You can derive the theoretical maximum by performing load testing with tools such as GuideLLM.  With GuideLLM you can create workloads that resemble your real world use case, and simulate concurrent connections, slowly ramping up the number of concurrent connections until you start to see performance degradation.  Based on that result, you can estimate the theoretical maximum number of tokens you can process in a period of time.  For example, if you were able to process 1M tokens per minute you could theoretically process 1,440M tokens per day.

In most scenarios you will not be able to sustain that level of maximum load 24/7, however it is useful for helping to understand if you are right sizing your deployments and doing planning for things like how many replicas you might need to meet your real world demand.  If you have built a system that can process 1,440M tokens per day, but you are only processing 50M, you may consider resizing your environment and finding ways to reduce the overall cost.

Measuring real world token processing is generally a better metric for deriving cost per token compared to the theoretical maximum.  By looking back at the real world usage you can better understand

### Optimizing Tokens Processed

The first thing that most teams turn towards when attempting to reduce cost is through optimization their model deployments.  One important consideration is that optimizing your model deployment impacts your theoretical maximum and not your actual processed tokens.  If I am able to optimize my deployment to be able to go from 1,440M to 1800M tokens per day, I have increased by total theoretical maximum by 25%, but if that performance gain doesn't also correspond to an increase in real world usage as well, their is no impact to the actual cost per token.

By optimizing model deployments, you can enable the onboarding of additional use cases, or help to grow the usage of an existing use case without adding additional hardware.  Alternatively, you may be able to scale down your existing workloads to use few resources.

However, the biggest impact organizations will see for reducing cost per token, is by increasing overall usage.  If your system is capable of processing 1440M tokens per day, but you are only processing 500M, you will see more impact to the total cost per token by driving more use cases onto the system.  Additionally, it may be helpful to find ways to better utilize the system in non-peak hours.  Shift batch workloads to off hours can help to better utilize the hardware while keeping performance high for peak usage times.

## The Impact of Model Choice

The model you choose to deploy will often have significant impact to both the cost through the hardware needed to support the model, and the performance of that model.

A model such as [Llama-3.1-8B-Instruct](https://huggingface.co/meta-llama/Llama-3.1-8B-Instruct) is significantly smaller than [Llama-3.3-70B-Instruct](https://huggingface.co/meta-llama/Llama-3.3-70B-Instruct).  The 8B model can easily fit on a single H100, or even potentially a more budget GPU like an L40S, while the 70B model may require up to four H100s to serve a single instance of the model.

Alternatively you may consider quantized versions of models.  An fp8 version of the 70B model could be deployed on two 

## Input Tokens, Cached Tokens, and Output Tokens

When dealing with cloud providers, you will often see different prices for models depending on the type of tokens being generated.

Input tokens are generally processed in a single pass and allow model servers like vLLM to take maximum advantage of it's continuous batching system and are highly parallelized.

Cached tokens are tokens that have already been computed and are available on the GPUs KV Cache.  vLLM is often able to take advantage of cached tokens when queries have a common prompts that provide instructions for how the LLM should behave, or in "multi-turn" conversations where things like chat history from a long running conversation are included in each LLM query.  Cached tokens are generally very cheap since the value is simply looked up, instead of needing to be re-processed by the GPU.

Tools like LLM-D help to increase the likelihood that requests will be able to get a KV Cache hit through capabilities like intelligent routing when running multi-replica deployments.

Unlike input tokens, output tokens are highly iterative.  Each output token is predicted one and a time.  This iterative process generally makes output tokens more expensive.

Speculative decoding is one option that can help to reduce the overall cost of output tokens.  With speculative decoding you use a smaller model to predict multiple tokens at once, and use the larger model to verify those predictions.  If the larger model disagrees with the smaller model, the tokens are rejected and regenerated.  This enables the model server to generate output tokens faster while still maintaining the exact same output results.

## Final Thoughts

Self-hosted LLM pricing is less about a sticker price per million tokens and more about understanding what you spend and how much you actually serve. Cost per token comes down to total operating cost—hardware, software, people, and whatever else you choose to include—divided by the tokens you process over that same period. You can improve that number by cutting spend through right sizing and autoscaling, by increasing real-world utilization so idle capacity is put to work, or by choosing models and serving techniques that better match your workload.

The most useful takeaway is to measure both sides of the equation. Track actual tokens processed—not just theoretical maximum throughput and account for how input, cached, and output tokens behave differently under vLLM. With that visibility, model choice, quantization, speculative decoding, and tools like LLM-D become deliberate levers for cost rather than guesswork, and you can compare self-hosted economics against managed APIs on equal footing.

