---
layout: default
title: Archive
permalink: /blog/archive/
---

<div class="blog-page">
  <header class="blog-header">
    <a href="/" class="back-link">← Back to portfolio</a>
    <h1>Archive</h1>
    <p>Browse all posts by month and year.</p>
  </header>

  <div class="archive-list">
{% assign postsByYearMonth = site.posts | group_by_exp: "post", "post.date | date: '%B %Y'" %}
{% for yearMonth in postsByYearMonth %}
  <div class="archive-group">
    <h2 class="archive-month">{{ yearMonth.name }}</h2>
    <ul class="archive-posts">
      {% for post in yearMonth.items %}
      <li>
        <a href="{{ post.url | relative_url }}">
          <span class="archive-title">{{ post.title }}</span>
          <span class="archive-date">{{ post.date | date: "%d %b" }}</span>
        </a>
      </li>
      {% endfor %}
    </ul>
  </div>
{% endfor %}
  </div>
</div>
