---
layout: default
title: Høy på sopp
parent: Beat Saber
nav_order: 2
---

# Høy på sopp

Sanger hvor det visuelle er hovedpoenget. De kan være utfordrende å spille, men det er ikke lasersverdene man er her for å se.

{% assign energetic_songs = site.songs | where: "vibe", "Visuell" %}
{% for song in energetic_songs %}
  <div>
  <h3><a href="{{ song.url }}">{{ song.artist }} - {{ song.title }}</a></h3>
    {% for difficulty in song.difficulties %}
    <ul>
      <li>
      <div>
      <p>{{difficulty.date}}</p>
      <iframe width="560" height="315" src="{{difficulty.video_url}}" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" allowfullscreen></iframe>
      </div>
      </li>
    </ul>
  {% endfor %}
  </div>
{% endfor %}

