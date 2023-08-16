# Working with Data Science Pipelines - Executing Pipelines with Kubeflow Pipelines

Red Hat OpenShift Data Science, part of OpenShift.AI, introduced Data Science Pipelines in RHODS 1.x.  Data Science Pipelines is Red Hat's enterprise ready, multi-tenant implementation of Kubeflow Pipelines, built on top of Tekton as the execution engine.

For this tutorial we will start with a simple 

## A Simple Pipeline

For this example we will be working with the `kfp` and `kfp_tekton` in a native python application.

At the time of writing this, Data Science Pipelines uses `kfp_tekton` 1.5.  Newer versions of the `kfp_tekton` package are not backwards compatible with the current version of Data Science Pipelines.  The following command will install the latest version of `kfp_tekton` 1.5 in your client environment and the latest version of `kfp` that is compatible with `kfp_tekton`.

```sh
pip install kfp_tekton~=1.5.0 kfp
```

In our pipeline, we will use the `kfp` package to construct our pipeline, and `kfp_tekton` to communicate with the Data Science Pipelines server.

To begin, we will create a new file called `add_pipeline.py` and we will import the packages:

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

Alternatively we could build our own image with additional python packages already installed if we need additional packages in the step.  The `create_component_from_func` function also provides us additional configuration options, including the `packages_to_install` parameter that will allow kfp to install additional packages during the execution of the step.

Finally, we can compose our pipeline using `add_op` as the different steps in our pipeline.  The `@kfp.dsl.pipeline` decorator allows us to easily convert a standard function into 

```python
@kfp.dsl.pipeline(
    name="Add Pipeline",
    description="A pipeline that adds numbers together",
)
def add_pipeline(a="1", b="7"):
    first_add_step = add_op(a, 4)
    second_add_step = add_op(first_add_step.output, b)
```

## Three Methods for Executing a Pipeline

Next we will look at three different methods for taking the pipeline we composed above and executing them in Data Science Pipelines.

In the previous steps we leveraged the `kfp` package to compose our pipeline.  In the following examples we will leverage the `kfp_tekton` package to help us compile or communicate with the Data Science Pipeline server directly.

### Generating a YAML Object

For the first option, we will be using `kfp_tekton` to compile the pipeline into a YAML object that can be manually uploaded into the RHODS Dashboard.  Once the pipeline has been uploaded, the pipeline can be executed, or scheduled to run on a set interval.

To generate the YAML file, we can add the following to the `add_pipeline.py` file we created before:

```python
if __name__ == "__main__":
    kfp_tekton.compiler.TektonCompiler().compile(
        add_pipeline, package_path=__file__.replace(".py", ".yaml")
    )
```

Next we can execute the file to generate a new file called `add_pipeline.yaml`:

```sh
python add_pipeline.py
```

The newly created `app_pipeline.yaml` file will contain a Tekton PipelineRun object that can now be uploaded to the RHODS Dashboard.

Using the project we created in part one, from the Data Science Pipelines > Pipelines section click on the option to `import pipeline`:

![Import Pipeline](images/import-pipeline.png)

Next, enter a pipeline name and description, then click on the `upload` and navigate to the `add_pipeline.yaml` file created in the previous step.

![Upload Pipeline](images/upload-pipeline.png)

After the pipeline has been successfully uploaded, you can now create a new run of the pipeline.  Click on the `>` to expand the pipeline and click `Create run`.

![Create Pipeline Run](images/create-run.png)

Enter a name for the run and click `Create`.

![Start Pipeline Run](images/create-run-2.png)

A new pipeline run will execute our add pipeline.

#### When to Use this Option

The option to generate a pipeline as a YAML object is one of the easiest and most straight forward ways of working with Data Science Pipelines.  It is a great option when attempting to test out an initial pipeline or validating if a pipeline will execute correctly.

In the case that a pipeline is not expect to change regularly or the pipeline is expected to be configured as a scheduled job without any regular updates, this option is generally the easiest and fastest way to accomplish those goals.

However, due to the number of manual steps needed to upload and execute a pipeline it is generally not a great option beyond a simple proof of concept in most cases and one of the following options is generally recommended.

### Submitting a Run from Python

Instead of compiling our pipeline into a YAML object, `kfp_tekton` provides the ability to create a client connect

```python
if __name__ == "__main__":
    kfp_tekton.compiler.TektonCompiler().compile(
        add_pipeline, package_path=__file__.replace(".py", ".yaml")
    )
```

### Uploading a Pipeline From Python and Trigger a Run