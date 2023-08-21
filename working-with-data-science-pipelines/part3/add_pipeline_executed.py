import kfp
import kfp_tekton

def add(a: float, b: float) -> float:
    """Calculate the sum of the two arguments."""
    return a + b

add_op = kfp.components.create_component_from_func(
    add,
    base_image="image-registry.openshift-image-registry.svc:5000/openshift/python:latest",
)

@kfp.dsl.pipeline(
    name="Add Pipeline",
    description="A pipeline that adds numbers together",
)
def add_pipeline(a="1", b="7"):
    first_add_step = add_op(a, 4)
    second_add_step = add_op(first_add_step.output, b)

if __name__ == "__main__":
    client = kfp_tekton.TektonClient(
        host="https://ds-pipeline-pipelines-definition-pipeline-demo.apps.cluster-q9bcd.q9bcd.sandbox493.opentlc.com",
        existing_token="sha256~ZenMMDSu6YD6GAjv49alq2kkGebpCoLb7crAZcXk5Do",
    )

    arguments = {"a": "7", "b": "8"}
    client.create_run_from_pipeline_func(
        add_pipeline, arguments=arguments, experiment_name="submitted-example"
    )
