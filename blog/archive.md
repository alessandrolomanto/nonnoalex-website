---
layout: default
title: Archive
description: The NonnoAlex archive, every note by month.
permalink: /blog/archive/
---

<header class="wrap page-head">
  <p class="label">Rack 01 · cold storage</p>
  <h1>Archive</h1>
  <p>Every note by month. The same list lives on the <a href="/blog/">notes</a> page.</p>
</header>

<div class="wrap">
  <div class="rack notes-rack">
    <ol class="units" aria-label="Archive by month">
{%- assign postsByYearMonth = site.posts | group_by_exp: "post", "post.date | date: '%B %Y'" -%}
{%- assign i = 0 -%}
{%- for yearMonth in postsByYearMonth %}
      <li class="blank"><span>{{ yearMonth.name }}</span></li>
  {%- for post in yearMonth.items %}
      <li>{% include unit.html post=post i=i %}</li>
      {%- assign i = i | plus: 1 -%}
  {%- endfor -%}
{%- endfor %}
    </ol>
  </div>
</div>
