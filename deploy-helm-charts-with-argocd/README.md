# Deploying Helm Charts with OpenShift GitOps

ArgoCD and its supported tools provide a number of different patterns that users can utilize for deploying helm resources.

1) Argo App pointing at a chart in a Helm repo
2) Argo App pointing at a chart in a git repo
3) Argo App pointing at a kustomize overlay rendering a chart

## Argo App Pointing at a Chart in a Helm Repo

The first option for deploying a helm chart is by referencing a chart that is hosted in a Helm Repository.

When deploying a chart from the ArgoCD UI, users provide a URL to the Helm Repo containing a collection of charts and selects the `Helm` option in the `Source` menu.  The `Chart` and `Version` fields will provide a list available options from a dropdown menu to select from.

![helm-repo-deployment](images/argo-helm-repo-ui.png)

Once the a chart has been entered in the `Source` section, a `Helm` section will become available, allowing the user to specify a values file, values in a YAML format, or by directly editing the default parameters auto-populated from the chart.

![helm-chart-parameters](images/argo-helm-values-ui.png)

> Tip
>
> As of OpenShift GitOps v1.8, you are only able to select a values.yaml packaged in the Helm Repo.  In future releases, Argo will support utilizing a `values.yaml` file located in a different git repository.

### Advantages

Deploying a chart directly from a Helm Repo provides a simple and intuitive user experience when utilizing the UI for deploying the chart.  The UI's auto-population of the default parameters helps to expose configurable options to the end users and avoid any mistakes such as misspelled parameter names.

### Disadvantages

This option makes it challenging to troubleshoot or render a helm chart from a development machine with the `helm template` command.  Any parameters that are populated in the UI are added into the Argo Application object which can be manually duplicated on the command line when running `helm template`.  The future option to add a `values.yaml` file from a separate git repo does greatly improve the ability to render the chart locally, but it can leave the `values.yaml` file orphaned in the git repo without any additional context, such as the chart repo, name, and version.

### Other Considerations

Deploying the chart directly from a Helm Repo is best for deploying charts that are well maintained, documented and require minimal troubleshooting.  This option is great for rapid deployment/prototyping of charts or "set it and forget it" deployments.

The challenges of rendering the chart locally can make this option especially challenging when developing custom charts.

## Argo App Pointing at a Chart in a Git Repo



### Advantages

### Disadvantages

### Other Considerations

## Argo App Pointing at a Kustomize Overlay Rendering a Chart

### Advantages

### Disadvantages

### Other Considerations


