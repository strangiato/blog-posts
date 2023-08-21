import kfp
import kfp_tekton

def add(a: float, b: float) -> float:
    """Calculate the sum of the two arguments."""
    return a - b

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

    kfp_tekton.compiler.TektonCompiler().compile(
        add_pipeline, package_path=__file__.replace(".py", ".yaml")
    )

    pipeline_id = client.get_pipeline_id(__file__.replace(".py", ".yaml"))

    pipeline_version = client.upload_pipeline_version(
        __file__.replace(".py", ".yaml"), 
        pipeline_version_name = "test2", 
        pipeline_id = pipeline_id,
    )

    print(client.list_pipeline_versions(pipeline_id=pipeline_id))
