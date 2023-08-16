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
    kfp_tekton.compiler.TektonCompiler().compile(
        add_pipeline, package_path=__file__.replace(".py", ".yaml")
    )