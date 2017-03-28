---
title: Getting Started with the test set
keywords: documentation
author: Bo Gao
summary: "A beginner's guide to the test set"
sidebar: t1_sidebar
permalink: t1_getting_started.html
folder: product1
---

## Introduction 

*Traffic Control Test Set* is a library of SUMO network models that are used as test beds for Traffic Control Systems. In this document, we give details on the current state of the project. As the project progresses, this guide will be updated accordingly.


## File Structure
At the current state of the project, we categorise our network models by their grid size

<pre>
model_libs
+-- 1x1
|   +-- 01
|   |   +-- data
|   |   |   +-- district.matrix
|   |   |   +-- model.<b>nod</b>.xml
|   |   |   +-- model.<b>edg</b>.xml
|   |   |   +-- model.<b>netccfg</b>
|   |   |   +-- model.<b>net</b>.xml
|   |   |   +-- model.svg
|   |   +-- {Traffic Controller API scripts}
|   +-- 02
|   +-- 03
|   ...
+-- 1x2
+-- 1x3
...
</pre>

## Example Model

Now, let's assume that we want to build a SUMO network model like the one shown below:


## How to Find a Model



{% include links.html %}
