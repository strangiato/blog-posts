# Deploying Helm Charts with OpenShift GitOps

ArgoCD and its supported tools provide a number of different patterns that users can utilize for deploying helm resources.

1) Argo App pointing at a chart in a Helm repo
2) Argo App pointing at a chart in a git repo
3) Argo App pointing at a kustomize overlay rendering a chart

## Argo App Pointing at a Chart in a Helm Repo

The first option for deploying a helm chart is by referencing a chart that is hosted in a Helm Repository.

When deploying a chart from the ArgoCD UI, users provide a URL to the Helm Repo containing a collection of charts and selects the `Helm` option in the `Source` menu.  The `Chart` and `Version` fields will provide a list available options from a dropdown menu to select from.

![helm-repo-deployment](images/argo-helm-repo-ui.png)

Once the a chart has been entered in the `Source` section, a `Helm` section will become available, allowing the user to specify a values file, 

> Tip
>
> As of OpenShift GitOps v1.x, you are only able to select a values.yaml packaged in the Helm Repo.  In future releases, Argo will support utilizing a values.yaml file located in a different git repository.

Argo will auto detect the available values and the defaults.  The intuitive user experience provides 

As of OpenShift GitOps 1.x, users can provide a values.yaml file separate from the helm repo location, making it easier to maintain the helm values outside of the ArgoCD application

### Advantages

Deploying a chart directly from a Helm Repo is the simplest and most straight forward method for deploying a Helm chart in ArgoCD.  

### Disadvantages

Deploying a chart directly from a Helm Repo provides the least native Helm experience and can be the most challenging option when troubleshooting.  Since the chart details and values settings are imbedded in the Argo Application object, it can be difficult to render the chart locally using `helm template`.

### Other Considerations

This option is best for deploying charts that are well maintained, documented and require minimal troubleshooting.  The challenge of 

## Argo App Pointing at a Chart in a Git Repo



### Advantages

### Disadvantages

### Other Considerations

## Argo App Pointing at a Kustomize Overlay Rendering a Chart

### Advantages

### Disadvantages

### Other Considerations


