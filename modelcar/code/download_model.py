from huggingface_hub import snapshot_download

model_repo = "ibm-granite/granite-3.0-2b-instruct"

snapshot_download(
    repo_id=model_repo,
    local_dir="./models",
    allow_patterns=["*.safetensors", "*.json", "*.txt"],
)
