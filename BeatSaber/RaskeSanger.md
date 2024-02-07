---
layout: default
title: Raske sanger
parent: Beat Saber
nav_order: 1
---

# Raske Sanger

Raske sanger, eller hvertfall kommer blokkene raskt. Kategorisert etter hvor jævlige de er å høre på:

1. [Ganske tolererbare](/BeatSaber/RaskeSanger.html#ganske-tolererbare)
2. [I grenseland](/BeatSaber/RaskeSanger.html#i-grenseland)
3. [Kan dette kalles musikk?](/BeatSaber/RaskeSanger.html#kan-dette-kalles-musikk)

Skal nevnes at det er noe helt annet når man står i det, da virker ikke sangene så jævlig. Men hører det jo i etterkant.

## Ganske tolererbare

{% assign energetic_songs = site.songs | where: "vibe", "Raske sanger" | where: "tolererbarhet", "Ganske tolererbar" %}
{% for song in energetic_songs %}
  <div>
  <h3><a href="{{ song.url }}">{{ song.artist }} - {{ song.title }}</a></h3>
    {% for difficulty in song.difficulties %}
    <ul>
      <li><b>{{difficulty.difficulty}}</b> {{difficulty.date}}</li>
    </ul>
  {% endfor %}
  <iframe style="border-radius:12px" src="{{ song.spotifypreviewurl }}" width="100%" height="152" frameBorder="0" allowfullscreen="" allow="autoplay; clipboard-write; encrypted-media; fullscreen; picture-in-picture" loading="lazy"></iframe>
  </div>
{% endfor %}

---

## I grenseland


{% assign energetic_songs = site.songs | where: "vibe", "Raske sanger" | where: "tolererbarhet", "I grenseland" %}
{% for song in energetic_songs %}
  <div>
  <h3><a href="{{ song.url }}">{{ song.artist }} - {{ song.title }}</a></h3>
  {% for difficulty in song.difficulties %}
    <ul>
      <li><b>{{difficulty.difficulty}}</b> {{difficulty.date}}</li>
    </ul>
  {% endfor %}

  <iframe style="border-radius:12px" src="{{ song.spotifypreviewurl }}" width="100%" height="152" frameBorder="0" allowfullscreen="" allow="autoplay; clipboard-write; encrypted-media; fullscreen; picture-in-picture" loading="lazy"></iframe>
  </div>
{% endfor %}

---

## Kan dette kalles musikk?

{% assign energetic_songs = site.songs | where: "vibe", "Raske sanger" | where: "tolererbarhet", "Er dette musikk" %}
{% for song in energetic_songs %}
  <div>
  <h3><a href="{{ song.url }}">{{ song.artist }} - {{ song.title }}</a></h3>
    {% for difficulty in song.difficulties %}
    <ul>
      <li><b>{{difficulty.difficulty}}</b> {{difficulty.date}}</li>
    </ul>
  {% endfor %}
  <iframe style="border-radius:12px" src="{{ song.spotifypreviewurl }}" width="100%" height="152" frameBorder="0" allowfullscreen="" allow="autoplay; clipboard-write; encrypted-media; fullscreen; picture-in-picture" loading="lazy"></iframe>
  </div>
{% endfor %}
