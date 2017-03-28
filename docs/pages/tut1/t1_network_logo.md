---
title: Interactive Network Logo (INL)
keywords: documentation
author: Bo Gao
summary: "Introducing the Interactive Network Logo"
sidebar: t1_sidebar
permalink: t1_network_logo.html
folder: documentation
---

## What is an Interactive Network Logo? {#what-is}

The objective of our project is to create a library of SUMO network models that may be used as test beds for Traffic Control Systems. This library will include tens if not hundreds of SUMO network definitions, therefore **navigating this library may be a challenging task with existing methods**. Currently, the only way to visually observe a network model is to open it with tools such as `sumo-gui`. This method has many disadvantages that work against the nature of our project:

- For a user to look up the library for a particular network model, it is not practical to manually download each model and observe its structure using `sumo-gui`.
- Existing methods use screenshots to illustrate the structure of the network. The size of our library and the potential requirement for its update prohibit the use of such manual step in the library's construction workflow.
- Screenshots only give limited amount of information about the network model. Information such as the `ID` of the nodes and edges are not displayed.

Therefore we implemented the production of an Interactive Network Logo into the network construction workflow so that the user may have direct access to the model structure before accessing the model files.

Provided that you have a good understanding of the [Network Definition Matrix](t1_network_definition_matrix.html) and its 8-directional unit structure, the logo is self-explainatory. In this document, we use an example network to demonstrate its usage and features. Being an ongoing project, as development of this project progresses, this guide will be updated accordingly.

## Example Logo {#example}

Below is the logo of a 5 x 5 network.

{% include svg.html file="network_logo_1.svg" %}

You can see the IDs of each node by moving your mouse over the nodes. In the next phase of development, information of edges will be added to the mouse interaction.

The centre junction of each NPU may be defined as either a `priority` junction or a `traffic_light` controlled junction.

The 5 x 5 NDM for this network is given as:

```
0 p357 p15 p157 p1
p5 t1357 t15678 t1357 p157
0 p3457 t1357 t12357 t1358
p75 t1357 t13568 p1347 0
p35 p13458 0 p235 p15
```

If you are not familiar with this matrix definition, please read our introduction of the Network Definition Matrix [here](/t1_network_definition_matrix.html).

## Where to find this logo? {#where}
A file named `model.svg` is located in the `data` folder of each one of our network model

<pre>
model_libs
+-- 1x1
|   +-- 01
|   |   +-- data
|   |   |   +-- district.matrix
|   |   |   +-- model.nod.xml
|   |   |   +-- model.edg.xml
|   |   |   +-- model.netccfg
|   |   |   +-- model.net.xml
|   |   |   +-- <b>model.svg</b>
|   |   +-- {Traffic Controller API scripts}
|   +-- 02
|   +-- 03
|   ...
+-- 1x2
+-- 1x3
...
</pre>

## Future Developments {#future} 

The design priority of this logo presentation is to make the network lookup process simple, interactive, and user-friendly. More interactive elements such edge and lane information will be added to the logo.


{% include links.html %}
