### Prerequisites
[Jekyll](https://jekyllrb.com/docs/)


## Install dependencies
This website is built on Jekyll and uses its built-in SCSS compiler to generate our CSS. Before getting started, you'll need to install the Jekyll gem and related dependencies:

```bash
$ bundle install
```
### 3. Running locally

To see your Jekyll site, start a Jekyll server:

```bash
$ bundle exec jekyll serve
```

Open <http://localhost:4000> in your browser, and voilà.

https://github.com/andrewhwanpark/dark-poole

## Automated releases

Pushing a version tag builds the image and deploys the Helm chart through
Tailscale:

```bash
git tag v1.0.2
git push origin v1.0.2
```

Create a GitHub environment named `production` with these secrets:

- `DOCKER_USERNAME` and `DOCKER_PASSWORD`: credentials for
  `docker.nonnoalex.dev`.
- `TS_OAUTH_CLIENT_ID` and `TS_OAUTH_SECRET`: Tailscale OAuth client with
  `auth_keys` write access and permission to create ephemeral `tag:ci` nodes.
- `KUBE_CONFIG`: a namespace-scoped kubeconfig that connects to the node's
  Tailscale IP and verifies the k3s certificate with `tls-server-name`.

Add this environment variable:

- `K3S_TAILSCALE_HOST`: the node's Tailscale IP or MagicDNS name.

Allow `tag:ci` to reach the k3s node on TCP 6443 in the tailnet policy. If the
kubeconfig uses a MagicDNS name, include that name in the k3s `tls-san`
configuration so Kubernetes certificate verification remains enabled.
