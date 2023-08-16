# Working with Data Science Pipelines - Executing Pipelines with Elyra

Red Hat OpenShift Data Science, part of OpenShift.AI, introduced Data Science Pipelines in RHODS 1.x.  Data Science Pipelines is Red Hat's enterprise ready, multi-tenant implementation of Kubeflow Pipelines, built on top of Tekton as the execution engine.

For this tutorial we will start with a simple 

## Creating a Data Science Pipeline Instance

Data Science Pipelines 

## A Simple Pipeline

For this example we will need a few Python packages.

At the time of writing this, Data Science Pipelines uses `kfp_tekton` 1.5.  Newer versions of the `kfp_tekton` package are not backwards compatible with the current version of Data Science Pipelines.  The following command will install the latest version of `kfp_tekton` 1.5 in your client environment and the latest version of `kfp` that is compatible with `kfp_tekton`.

```sh
pip install kfp_tekton~=1.5.0 kfp
```

In our pipeline, we will use the `kfp` package to construct our pipeline, and `kfp_tekton` to communicate with the Data Science Pipelines server.

To begin, we will import the packages:

```python
import kfp
import kfp_tekton
```

Next we will create a simple add function:

```python
def add(a: float, b: float) -> float:
    """Calculate the sum of the two arguments."""
    return a + b
```

We will then use that add function to create a kfp component.  A component is a self-contained step to be executed in our pipeline.  The component defines both the code to be executed (the `add` function from the previous step) and the image that will be used to execute the code.  In this case, we are using the Python image provided by OpenShifts built in container registry.

```python
add_op = kfp.components.create_component_from_func(
    add,
    base_image="image-registry.openshift-image-registry.svc:5000/openshift/python:latest",
)
```

Finally, we can compose `add_op` into multiple steps in our 

```python
@kfp.dsl.pipeline(
    name="Add Pipeline",
    description="A pipeline that adds numbers together",
)
def add_pipeline(a="1", b="7"):
    first_add_task = add_op(a, 4)
    second_add_task = add_op(first_add_task.output, b)
```


## Generating a YAML Object



```python
if __name__ == "__main__":
    kfp_tekton.compiler.TektonCompiler().compile(
        add_pipeline, package_path=__file__.replace(".py", ".yaml")
    )
```

## Submitting a Run from Python

## Uploading a Pipeline From Python