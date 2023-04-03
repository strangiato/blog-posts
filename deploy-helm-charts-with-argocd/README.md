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

This option makes it challenging to troubleshoot or render a helm chart from a development machine with the `helm template` command.  Any parameters that are populated in the UI are added into the Argo Application object which can be manually duplicated on the command line when running `helm template` but this option leaves room for errors and typos.  The future option to add a `values.yaml` file from a separate git repo does greatly improve the ability to render the chart locally, but it can leave the `values.yaml` file orphaned in the git repo without any additional context, such as the chart repo, name, and version.

This design pattern also does not allow for any flexibility or customization to objects deployed in the chart that are not explicitly allowed by the original chart author.  For example, if the original author of a chart does not include options to set a  `nodeSelector` in the values, users will not have the ability to set that option in a `Deployment`.

### Other Considerations

Deploying the chart directly from a Helm Repo is best for deploying charts that are well maintained, documented and require minimal troubleshooting.  This option is great for rapid deployment/prototyping of charts or "set it and forget it" deployments.

The challenges of rendering the chart locally can make this option especially challenging when developing custom charts.

When managing deployments of the chart to multiple environments with minimal differences the Argo Application file can easily be incorporated into a kustomize overlays pattern where the differences are patched for each environment.

## Argo App Pointing at a Chart in a Git Repo

Another option for deploying a helm chart with Argo is by generating a chart and storing it directly in a git repo.  When using this option, users will provide a git repo URL and the path to the `Chart.yaml` file.  Argo will automatically detect the helm chart and render the chart when deploying.

Charts stored in the git repo can be a fully self contained chart, utilizing templates, or it can take advantage of chart dependencies, to deploy either charts hosted in a Helm Repo or another chart in the same git repo.

To utilize a chart stored in a Helm Repo, you can provide the dependency information in the `Chart.yaml` object:

```
dependencies:
  - name: "mlflow-server"
    version: "0.5.7"
    repository: "https://strangiato.github.io/helm-charts/"
```

To reference another chart located in the same git repo, you can utilize the `file://` protocol in the `Chart.yaml` files repository field:

```
dependencies:
  - name: "my-local-chart"
    version: "0.1.0"
    repository: "file://../my-local-chart/"
```

Parameters can be configured in the local helm chart using the `values.yaml` file and Argo will automatically utilize this file when rendering the chart.

### Advantages

This design pattern provides the most native helm developer experience, and easily allows developers to take advantage of helms features such as `helm template` and `helm lint` in their local environment.

### Disadvantages

Like deploying a chart from a helm repo, if the original author does not provide an option to configure a specific setting, users will not have the ability to set those options.

This pattern can also create "junk" files for a simple deployment that may not necessarily be needed in the final git repo, such as `.helmignore`, `Chart.lock`, or dependent chart `*.tgz` files that have been downloaded locally for testing.  Some of these files may be added to the `.gitignore` file to reduce clutter in the repo.

### Other Considerations

This option is ideal for having maximum flexibility when developing a custom charts.  The ability to create a simple chart without needing to package and store it in a Helm Repo allows for extremely rapid prototyping.

Leveraging chart dependencies within the same git repo allow for a flexible pattern for building out a multi-tiered application deployment to different environments.  By creating a simple chart folder structure such as the one below, users are able to develop a custom chart for an application deployed to multiple environments and provide configuration differences in the environment-charts `values.yaml` file.

```
.
├── common-charts
│   └── my-application
└── environment-charts
    ├── dev
    │   └── my-application
    ├── prod
    │   └── my-application
    └── test
        └── my-application
```

If managing a chart with a more complex lifecycle, users are still able to utilize the same environment-charts pattern and instead leverage a Helm Repo to host and version their charts.

## Argo App Pointing at a Kustomize Overlay Rendering a Chart

### Advantages

### Disadvantages

### Other Considerations


