---
layout: default
title: Archive
permalink: /blog/archive/
---

<div class="blog-page">
  <header class="page-header">
    <h1>Archive</h1>
  </header>

  <div class="archive-list">
{% assign postsByYearMonth = site.posts | group_by_exp: "post", "post.date | date: '%B %Y'" %}
{% for yearMonth in postsByYearMonth %}
  <div class="archive-group">
    <h2 class="archive-month">{{ yearMonth.name }}</h2>
    <ul class="post-list">
      {% for post in yearMonth.items %}
      <li>
        <a href="{{ post.url | relative_url }}" class="post-row">
          <time>{{ post.date | date: "%d %b" }}</time>
          <span>{{ post.title }}</span>
        </a>
      </li>
      {% endfor %}
    </ul>
  </div>
{% endfor %}
  </div>
</div>
