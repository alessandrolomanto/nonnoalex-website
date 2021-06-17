---
layout: post
title: Tips and Tricks CKAD Exam
---
Kubernetes is the most famous open-source system for automating deployment, scaling, and management of containerized applications and the certification Certified Kubernetes Application Developer help you to have a complete environment for be able to design, build, configure and expose application created for cloud native.

It's a remote exam, **consist in ~19 hands-on questions in 2 hours.**
You may can think a person who daily work in this kind of tecnology can pass exams in very easy way. In reality, the real variable is time management.
In this article i want to share my experience and give some advise for pass the exams and optimize the time for preparation.

## Tips for studying

1. Udemy Course

    I bought this [course](https://www.udemy.com/course/certified-kubernetes-application-developer/) and followed all steps. At the end i did many times all mock exams and labs.

1. [Game of Pods](https://kodekloud.com/p/game-of-pods )

    Unfortunately i can't do this because was in develop, but i think its good way to learn as a game and improve skills having a complete overview.

1. Killer.sh (Day Before Exam)

    There are more complex exercises than the real exam, and the mock exam user interface is very similar to the real exam. They were helpful in preparing for the exam mentally and familiar with time management.

1. Github (Pay attention for Kubernetes version!)

    Github, there is no need for me to say it, it is truly a resource pit. If you try to type CKAD in the search bar, you will be spoiled for choice of how much material there is and how many people have been willing to take the time to help others. Let's do it!

## Practical advice for the exam

1. Shortcut #1 
    <pre class="highlight">
    <code class="language-bash" data-lang="bash">
        alias k=kubectl
    </code>
    </pre>


    *kubectl* is the command you will almost always use, try also to remember contract form of Kubernetes Object like following examples:
    <pre class="highlight">
    <code class="language-bash" data-lang="bash">
        k get po
        k get netpol
        k get svc
    </code>
    </pre>

1. Shortcut #2 
    <pre class="highlight">
    <code class="language-bash" data-lang="bash">
        export DRY="--dry-run=client -o yaml"
    </code>
    </pre>
    Although you can use the documentation to recover yaml, I recommend to use this command for creating and edit working yaml file:
    <pre class="highlight">
    <code class="language-bash" data-lang="bash">
        k run nginx --image=nginx $DRY > nginx.yaml
    </code>
    </pre>


1. Learning Vim is lifesaver

    Read this simple [article](https://blog.codonomics.com/2019/09/essential-vim-for-ckad-or-cka-exam.html) with all basic command that are very useful not only for the exam.

1. [Imperative command](https://kubernetes.io/docs/tasks/manage-kubernetes-objects/imperative-command/)

    Knowing the yaml is important but for the exam my advice is to exploit the imperative commands as much as possible, I think they are the thing that make the most difference in saving time.



## General advice and problems I have addressed

1. Test your webcam and make sure your documents are clearly visible.

    I bought a 1080p webcam but it was a flop because the proctor could not display the identification document numbers,
    I had to switch into the laptop's built-in one before moving on.

1. Create your browser favorites

    During the exam you have an additional tab to view the official k8s documentation.
    I found it convenient as I followed the courses and mocks to save the pages and organize them so that I could consult quickly.

1. Always check the namespace and cluster

    For the ckad there are 4 clusters, during the exam they will ask you to switch from one cluster to another as well as from one namespace to another.

1. Vim `set paste`

    When you copy and paste YAML segments, this could cause weirdly formatted config which could be a real pain during the exam where every second matters. 
    In order to avoid this, turn off auto indent when you paste code. There’s a special “paste” mode.
    Type
    <pre class="highlight">
    <code class="language-bash" data-lang="bash">
        :set paste
    </code>
    </pre>

    Then paste your code. Note that the text in the tooltip now says -- INSERT (paste) --.
    After pasting, turn off the paste-mode, so that auto-indenting when you type works correctly again.
    <pre class="highlight">
        <code class="language-bash" data-lang="bash">
            :set nopaste
        </code>
    </pre>

1. Mark questions to revisit later
Check the percentage value of the question, you can spend about 6 minutes.
You have the option to mark a question to revisit it later in case you have some doubts or issues. 
Do not get stuck in a question and spend a disproportionately long time on it but mark it and revisit it later.

![CKAD](/assets/images/CKAD.png)

My last advice create your local cluster and ***practice, practice and practice!***
