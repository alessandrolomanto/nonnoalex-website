---
layout: post
title: Run Claude Code safely with --dangerously-skip-permissions in k8s agents sandbox
image: /assets/images/dangerously-skip-permissions.png
---

Claude Code has a flag called `--dangerously-skip-permissions`, and it does exactly what the name says. The agent stops asking before it runs a shell command, edits a file, whatever. No prompts, no confirmations, just full autonomy.

Honestly, that's what you want once you're doing real work with it. Approving every single `ls` gets old within about five minutes.

The problem is running it like that on your laptop. One bad command and there go your files, your repos, your credentials.

I'll get to how I fixed that. First, the part that actually matters.

---

## Agents are workloads, not tools

Most people treat AI coding agents like a smarter autocomplete. You open a terminal, hand it your repo, and let it go. It feels like a tool because it answers when you prompt it.

But it isn't one. It's a process running arbitrary code with your permissions. The moment you start `claude` on your laptop, it inherits everything you have: your user, your SSH keys, your AWS credentials, your git config. Whatever it can reach, it can touch as you.

That's fine while you're watching. It gets a lot less fine the moment you walk away.

I've been moving toward AI infrastructure as a focus, and this is exactly where the infrastructure mindset earns its keep. The interesting question stopped being "how do I prompt this better?" and turned into "how do I box in a process that can do anything?"

## What containment looks like

In normal infrastructure you'd never run untrusted code as root on a production host. You drop it in a container, strip its capabilities, cap its resources, wall off the filesystem. None of this is new — the patterns have been around for decades, and they hold up.

Agents deserve the same handling. Not because they're malicious, but because they're unpredictable. One that can run `curl` can quietly ship your data somewhere. One that can write files can clobber your `.ssh/config`. One with no memory ceiling can take the whole machine down with it.

And the boundary can't be the agent's own permission prompts — that's asking a process to police itself. It has to come from outside: the operating system, or the orchestrator.

## k8s-agents-sandbox

So I built `k8s-agents-sandbox` to put this into practice. It's a small learning project, two skills and one example, but the principles are all in there.

You can install the skills with:

```bash
npx skills add alessandrolomanto/k8s-agents-sandbox
```

Or just clone the repo and point your agent at it.

The first skill, `install-kind-cluster`, stands up a local Kubernetes cluster. It checks whether `docker`, `kind`, and `kubectl` are around, installs whatever's missing, and waits until the nodes are actually ready.

Open your favorite coding agent and ask:

```plaintext
install a kubernetes cluster with 2 nodes
```

The second skill, `install-agent-sandbox`, installs the `agent-sandbox` CRD and controller from kubernetes-sigs. This gives you a `Sandbox` custom resource that manages pod lifecycle, stable identity, and crash recovery.

Ask:

```plaintext
install agent sandbox with claude code example
```

The example drops Claude Code into an Agent Sandbox with a hardened manifest — non-root user, every Linux capability dropped, no privilege escalation, read-only root filesystem, and so on.

Every setting is there for a reason. Running non-root with no capabilities means the agent can't tamper with the container or climb to root. The read-only root filesystem stops it from leaving behind a persistent backdoor or rewriting system binaries. Seccomp closes off the dangerous syscalls, and the resource limits keep a runaway process from eating the host. The `emptyDir` volumes give it scratch space to work in without ever touching the real filesystem underneath.

## Running it

Access the Kubernetes sandbox resource with:

```bash
kubectl exec -it pod/claude-code-sandbox -- claude
```

The first time you exec in, you log into Claude Code by hand. The credentials live in the `/workspace` volume and stay there. If the pod falls over, the controller brings it back with the same identity and the same workspace, intact.

## What this teaches

Building this shifted how I think about agents. None of the skills involved were new to me — container isolation, resource limits, least privilege, containing failure. It's the same work I've been doing on ordinary workloads for years.

What's different is the threat model. A web server has an attack surface you can more or less map out. An agent's is emergent: you can't list everything it might decide to do, so instead you pin down what it's *allowed* to do, down at the infrastructure layer.

And that's where infra people have a head start. You already know how to build these walls. You just point them at a new kind of workload.

## Back to --dangerously-skip-permissions

So, the payoff. Inside that hardened container, Claude Code can do whatever it likes:

```bash
kubectl exec -it pod/claude-code-sandbox -- claude --dangerously-skip-permissions
```

Run anything, install packages, clone repos, delete files — doesn't matter. It can't get to root, can't write outside its own volumes, can't burn past the resource limits, and can't call the syscalls seccomp has blocked.

And it can't phone home to wherever it likes. Egress is denied by default and opened only to a short allowlist — the Anthropic API, GitHub, the package registries it actually needs — enforced with domain-aware network policy. That closes the `curl` exfiltration risk I opened with: even a fully compromised agent has nowhere to ship your data. The allowlist becomes your trust boundary, so keep it short.

The container is the jail. `--dangerously-skip-permissions` just means you're not bothering to build a second jail inside the first one.

That's the part I want to get better at: the unglamorous infrastructure work that lets an agent run free without it turning into a risk.

The project is open source: [k8s-agents-sandbox](https://github.com/alessandrolomanto/k8s-agents-sandbox). Two skills, one example, no build system. If you're thinking about running agents safely, it's a starting point.

---

*This article was written with the help of AI*
