---
layout: post
title: Overkilled Infrastructure for a Blog
---
![INFRA](/assets/images/infra-blog.png)

___

Could I configure a website using nginx? Yes of course! But it wasn't funny.

___

I bought my little VPS with 2 CPU and 4GB Ram for "production" lab environment only for studying and testing stuff with real-world taste but... I needed a place for my *automated* Blog.

It won't be a deep dive tutorial for setting up this infrastructure because there are so many technologies and I want to create a little series of articles for each one of this.

***Let's start with my overkilled infrastructure!***
<br/><br/>
## Kubernetes Lightweight
___

 [K3s](https://k3s.io/) is a fully CNCF certified Kubernetes designed to be a single binary of less than 40MB that completely implements the Kubernetes API. 
I don't have a lot resources and i don't want to spend much money for creating a super infrastructure and K3s comes to help me.

It's really easy to install, just only one bash command:
```sh
curl -sfL https://get.k3s.io | sh -
```
After maybe 30 seconds

```sh
kubectl --kubeconfig /etc/rancher/k3s/k3s.yaml get node
```
[Documentation](https://rancher.com/docs/k3s/latest/en/quick-start/)
<br/><br/>

## [MetalLB](https://metallb.universe.tf/)
___

In traditional cloud environments load balancers are available on-demand by Cloud provider.
MetalLB provides a network load-balancer implementation for Kubernetes clusters that do not run on a supported cloud provider, effectively allowing the usage of LoadBalancer Services within any cluster.

MetalLB requires a pool of IP addresses in order to be able to take ownership of the traefik-ingress Service. This pool can be defined in a ConfigMap named config located in the same namespace as the MetalLB controller. This pool of IPs must be dedicated to MetalLB's use, you can't reuse the Kubernetes node IPs or IPs handed out by a DHCP server.

[Installation](https://metallb.universe.tf/installation/#installation-by-manifest)
<br/><br/>
## [Traefik](https://traefik.io/)
___
***Too much nginx! I'm kidding*** 😃

The ingress configuration specifies how to get traffic from outside our cluster to services inside it and k3s comes pre-configured with Traefik as an ingress controller.
Traefik can be disabled but i wanted to enter deep dive for trying nginx alternative.
This is my high level config:

1. Lets Encrypt
```yaml
additionalArguments:
  - --certificatesresolvers.letsencrypt.acme.tlschallenge=true
  - --certificatesresolvers.letsencrypt.acme.email= #email
  - --certificatesresolvers.letsencrypt.acme.storage=acme.json
  - --certificatesresolvers.letsencrypt.acme.caserver=https://acme-v02.api.letsencrypt.org/directory
```

1. Metrics
```yaml
additionalArguments:
  - --metrics.prometheus=true
  - --metrics.prometheus.entryPoint=metrics
  - --entryPoints.metrics.address=:8082
```

1. Dashboard
```yaml
additionalArguments:
 - --api.dashboard=true
```

1. BasicAuth middleware

The BasicAuth middleware restricts access to your services to known users. 
[Docs](https://doc.traefik.io/traefik/middlewares/basicauth/)
<br/><br/>
## Prometheus and Grafana
___

I deployed Prometheus and Grafana to monitor Kubernetes, traffic to my website and VPS hardware resources.

For me there are three pillars of observability: *Logging, Tracing and Metrics.* 

Traefik covers all features:

***APP LEVEL:*** Traefik provides three integrated features to have a clear overview of observability.
<p align="center">
  <img src="/assets/images/traefik-feature.png" />
</p>

***INFRA LEVEL:*** I installed `NodeExporter` in order to find the info on hardware resources.

[Docs](https://github.com/helm/charts/tree/master/stable/prometheus-node-exporter)

[Grafana Dashboard](https://grafana.com/grafana/dashboards/1860)

***ALARMS:*** I used `Grafana Alarm` and if the disk becomes full I get the notification with the Telegram bot.
<p align="center">
  <img src="/assets/images/telegram-notification.png" />
</p>
<br/><br/>
## [Harbor](https://goharbor.io/)
___
Harbor is one of the most successful open source projects from VMware. It is a cloud native registry that stores, signs and scans content, with the mission of providing cloud native environments the ability to confidently manage and serve container images.
Harbor supports features such as user management access control and activity auditing.

[Installation with Helm](https://goharbor.io/docs/2.3.0/install-config/harbor-ha-helm/)
<br/><br/>
## [Flux Helm Operator](https://fluxcd.io/legacy/helm-operator/)
___

Flux is based on a set of Kubernetes API extensions (“custom resources”), which control how git repositories and other sources of configuration are applied into the cluster (“synced”).

There are other tools available for continuous deployment like ArgoCD and there is no particular reason why I chose one over the other.
I installed `Helm Operator` that is a Kubernetes operator, allowing one to declaratively manage Helm chart releases.


The desired state of a Helm release is described through a Kubernetes Custom Resource named HelmRelease. Based on the creation, mutation or removal of a HelmRelease resource in the cluster, Helm actions are performed by the operator.

**Configuration:**
```yaml
apiVersion: helm.fluxcd.io/v1
kind: HelmRelease
metadata:
  name: nonnoalex-release
  namespace: flux
spec:
  chart:
    git: https://github.com/alessandrolomanto/nonnoalex-website
    ref: master
    path: helm/nonnoalex-website
```
[Install and examples](https://github.com/fluxcd/helm-operator/blob/master/chart/helm-operator/README.md)
<br/><br/>
## GitHub Actions
___

Jenkins? Tekton? Why install new components to put my little machine in pain since there is Github that can help me do this?

To be able to publish Docker images to my container registry, we need first authenticate with a valid account.

The pipeline is still not as I would like it because I want to push the images to the registry with both the version and the latest tag. 

Later I will see in depth the handle of the environment variables and the tags.
This is my configution available on [github](https://github.com/alessandrolomanto/nonnoalex-website/blob/master/.github/workflows/main.yml)

___

<br/><br/>
<h2><center>Enjoy this architecture for a simple blog using Jekyll!</center></h2>