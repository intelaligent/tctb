---
title: Glossary
keywords: documentation
author: Bo Gao
summary: "Project Glossary"
sidebar: home_sidebar
permalink: glossary.html
folder: documentation
---

<!-- | Term | Description |
{% for entry in site.data.glossary.glossary %}| {{entry.display_name}} | {{entry.description}} {% if entry.link %} <a href="{{entry.link}}">Read More</a> {% endif %}|
{% endfor%}  -->

<dl>{% for entry in site.data.glossary.glossary %}<dt id="{{entry.code_name}}">{{entry.display_name}}</dt><dd>{{entry.description}}{% if entry.link %} <a href="{{entry.link}}">Read More</a> {% endif %}</dd>{% endfor%} </dl>