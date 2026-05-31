---
layout: post
title: Run Claude Code safely with --dangerously-skip-permissions in k8s agents sandbox
---

Claude Code has a flag called `--dangerously-skip-permissions`. It does what it says. The agent stops asking before running shell commands, editing files, or doing anything else. No approval prompts, just full autonomy.

It's also exactly what you want if you're using Claude Code to do real work. Asking for permission every time the agent wants to run `ls` gets old fast.

But running it on your laptop like that is reckless. One bad command and it's your filesystem, your git repos, your credentials.

I'll come back to how I solved this. First, the bigger problem.

---

## Agents are workloads, not tools

Most people treat AI coding agents like a smarter autocomplete. You open a terminal, give it your repo, and let it work. It feels like a tool because it responds to your prompts.

It's not a tool. It's a process that executes arbitrary code with your permissions. When you run `claude` on your laptop, it inherits your user, your SSH keys, your AWS credentials, your git config. Anything it can do, it can do as you.

This is fine when you're watching. It's a problem when you're not.

I've been building toward AI infrastructure as a specialization, and this is where infrastructure thinking actually matters. The question isn't "how do I prompt better?" It's "how do I contain a process that can do anything?"

## What containment looks like

In traditional infrastructure, you don't run untrusted code as root on your production host. You put it in a container, drop capabilities, limit resources, and isolate the filesystem. These patterns are decades old. They work.

AI agents need the same treatment. Not because agents are malicious, but because they're unpredictable. An agent that can run `curl` can exfiltrate data. An agent that can write files can overwrite your `.ssh/config`. An agent with no memory limit can OOM your machine.

The security boundary shouldn't be the agent's own permission system. That's like trusting a process to police itself. The boundary should be external, enforced by the operating system or the orchestrator.

## k8s-agents-sandbox

I built `k8s-agents-sandbox` to apply this thinking. It's a small learning project, two skills and one example, but it encodes the principles.

You can install the skills with:

```bash
npx skills add alessandrolomanto/k8s-agents-sandbox
```

Or just clone the repo and point your agent at it.

The first skill, `install-kind-cluster`, provisions a local Kubernetes cluster. It checks for `docker`, `kind`, and `kubectl`, installs what's missing, and waits for the nodes to be ready.

Open your favorite coding agent and ask:

```plaintext
install a kubernetes cluster with 2 nodes
```

The second skill, `install-agent-sandbox`, installs the `agent-sandbox` CRD and controller from kubernetes-sigs. This gives you a `Sandbox` custom resource that manages pod lifecycle, stable identity, and crash recovery.

Ask:

```plaintext
install agent sandbox with claude code example
```

The example deploys Claude Code inside an Agent Sandbox with a hardened manifest (non-root user, all Linux capabilities dropped, no privilege escalation, read-only root filesystem, and so on).

Each of these controls addresses a specific risk. Non-root and dropped capabilities prevent the agent from modifying the container or escalating privileges. The read-only filesystem means the agent can't install persistent backdoors or modify system binaries. Seccomp blocks dangerous syscalls. Resource limits prevent runaway processes. The `emptyDir` volumes give the agent somewhere to work without access to the host filesystem.

## Running it

Access the Kubernetes sandbox resource with:

```bash
kubectl exec -it pod/claude-code-sandbox -- claude
```

The first time you exec in, you log in to Claude Code interactively. Credentials stay inside the `/workspace` volume. If the pod crashes, the controller brings it back with the same identity and workspace intact.

## What this teaches

Building this changed how I think about AI agents. The relevant skills aren't new. Container isolation, resource limits, least privilege, failure containment — these are the same things I've been doing with regular workloads for years.

The difference is the threat model. A web server has a known attack surface. An AI agent has an emergent one. You can't enumerate everything it might do, so you constrain what it's allowed to do at the infrastructure level.

This is where infrastructure people have an advantage. You already know how to build these boundaries. You just need to apply them to a new kind of workload.

## Back to --dangerously-skip-permissions

So here's the payoff. Inside that hardened container, Claude Code can do whatever it wants:

```bash
kubectl exec -it pod/claude-code-sandbox -- claude --dangerously-skip-permissions
```

Run any command, install packages, clone repos, delete files. It doesn't matter. The agent can't escalate to root, can't write outside its sandboxed volumes, can't consume more resources than the limits, and can't make syscalls that seccomp blocks.

The container is the jail. `--dangerously-skip-permissions` just means you're not putting a second jail inside the first one.

That's the part I want to get better at. The boring infrastructure work that lets an agent have freedom without the risk.

The project is open source: [k8s-agents-sandbox](https://github.com/alessandrolomanto/k8s-agents-sandbox). Two skills, one example, no build system. If you're thinking about running agents safely, it's a starting point.

---

*This article was written with the help of AI, of course.*
