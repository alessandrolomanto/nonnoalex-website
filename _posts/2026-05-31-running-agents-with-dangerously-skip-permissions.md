---
layout: post
title: Run Claude Code safely with dangerously-skip-permissions in k8s agents sandbox
image: /assets/images/dangerously-skip-permissions.png
---

`--dangerously-skip-permissions` does exactly what it says. No prompts, no confirmations, the agent just runs whatever it decides.

After five minutes of approving every `ls` you want exactly that. But on a laptop? Your SSH keys, your AWS credentials, your git config. All of it one bad prompt away. I looked at that flag and closed the terminal.

I needed a way to run it where it couldn't touch anything that mattered.

## Docker, almost

First thing I tried was putting it in a container. `docker run --rm -it`. Agent can't see my laptop filesystem. I thought I solved it in ten minutes.

Then I checked the files it wrote. Every single one owned by root on my host overlay. I tried to clean up, `rm` said permission denied. The container runs as root by default. I never thought to check.

Spent twenty minutes doing `sudo chown -R` on my own directories. Added `RUN useradd` and `USER` to the Dockerfile and moved on. The user has no real home directory, the shell config is half broken. I don't care enough to fix it. The container works.

But it's still too thin. No resource limits. No crash recovery. No real network policy. A runaway agent eats the whole machine. I wanted Kubernetes for that.

## k8s-agents-sandbox

Two skills, one example manifest. That's the whole project.

First skill installs a local cluster with `kind`. It checks for docker, kind, kubectl, installs what's missing, waits for nodes to report ready.

```plaintext
install a kubernetes cluster with 2 nodes
```

Second skill installs the `agent-sandbox` CRD and controller from kubernetes-sigs. It gives you a `Sandbox` resource that manages pod lifecycle. Stuff you need but don't want to think about.

```plaintext
install agent sandbox with claude code example
```

The manifest drops Claude Code into a hardened pod. Non-root user. All capabilities dropped. No privilege escalation. Read-only root filesystem. CPU and memory limits. I started with `RuntimeDefault` for seccomp and that worked fine. Then I tried a custom profile. The pod refused to start with "cannot create container." No hint about which syscall. Turns out `mount` is needed for `emptyDir` volumes. Took me a while. I went back to `RuntimeDefault`.

## Network

This part I kept coming back to. Egress denied by default. I open only the Anthropic API, GitHub, npm, PyPI. Domain-aware network policy.

If the agent gets compromised there's nowhere it can ship data. The allowlist is the boundary. Every domain you add widens the hole. I keep mine short.

Access the sandbox with:

```bash
kubectl exec -it pod/claude-code-sandbox -- claude --dangerously-skip-permissions
```

First login is manual. Credentials go to `/workspace`, persistent volume. Pod dies, controller brings it back. Login survives a crash.

## This is overkill

Kubernetes for one agent on one laptop is stupid. Docker with `--user`, `--read-only`, `--cap-drop=ALL` gets you most of the way. I used k8s because I was thinking about multiple agents, multiple users, shared clusters, isolation between tenants. I don't have that problem yet.

I built it anyway because I wanted to see what breaks before it matters.

One thing I realized while building this: securing an agent is not like securing a web server. A web server has ports, protocols, endpoints. You list them, lock them down, done. An agent might do anything. That's the point. So you stop trying to predict what it does and you limit what it's allowed to do at the OS layer. Not a new idea. Same pattern I use for any untrusted workload. I just never applied it to a coding agent before.

The project is [k8s-agents-sandbox](https://github.com/alessandrolomanto/k8s-agents-sandbox).

---

*Written with help from AI*
