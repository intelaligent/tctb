---
title: Network Definition Matrix (NDM)
keywords: documentation
author: Bo Gao
summary: "Introducing the Network Definition matrix"
sidebar: t1_sidebar
permalink: t1_network_definition_matrix.html
folder: documentation
---

## Purposes and Features {#purposes-and-features}

The objective of our project is to create a library of SUMO network models that may be used as test beds for Traffic Control Systems. **The first step towards this goal is to define a collection of networks** that are compatible with SUMO. Existing approaches to this end include:

1. Manually produce the XML files required by SUMO
   - This approach requires manual editing of XML files.
   - Provided that the user is familiar with the format, the difficulty of this approach increases as the size of the network increases.
   - Modifications to networks is difficult to implement.
2. Use the [NETEDIT](http://sumo.dlr.de/wiki/NETEDIT) tool to produce and modify the XML files of a network
   - The NETEDIT tool provides a GUI for network editing but the tool itself comes with a steep learning curve.
   - Making a relatively simple network takes more effort than necessary using the NETEDIT tool
   - The end product does not manifest itself well with an application interface which we plan to develop as part of this project.
3. Import networks from [a list](http://sumo.dlr.de/wiki/NETCONVERT) of supported software formats.
   - This approach is more suited large scale network model are imported whereas what we are looking to build is a series of abstract networks of compact sizes

After reviewing these existing approaches, we identified the need for a simpler network definition format the key requirements of which are:

1. Strong human-readability
2. SUMO-compatible
3. Extensible to the future development of traffic control APIs

In this document, we give details on the new format we proposed incorporating all of these features. Being an ongoing project, development progresses, this guide will be updated accordingly.

## Network Profile Unit

One key concept of our definition matrix is the use of an eight-directional unit as the building block for the construction of network models. This basic unit's profile is illustrated as below:

![matrix unit profile](images/matrix_definition_2.svg)

This is a square-shaped unit which contains eight roads/edges connecting the centre of the square to the eight directional points of the square. Our network definition matrix is a collection of this unit in a space-delimited matrix formation. We demonstrate the application of this profile with an example.

## Building an Example Model

Let us assume that we want to build a SUMO network model like the one shown below:

![wanted network](images/matrix_definition_1.svg)

The process of writing the matrix definition of this network includes two steps:

**A**: We divide this network to smaller units that can be described by our profile unit. In this example, this means dividing the network into six pieces of squares illustrated by the coloured lines as below:

![divided network](images/matrix_definition_3.svg)

**B**: For each square unit, we write down its representation according to the matrix unit's profile. In this example, the corresponding matrix is:

```
p1357 p157 p13578
0 p13574 p1357
```

Which produces a network represented by the following logo:

{% include svg.html file="matrix_definition_example_1.svg" %}

Note:

- Because there is nothing in the 4th square a space holder `0` is given in place of a unit's description
- The default description of each square unit begins with a `p` for `priority` junctions
- The order in which the edges/roads' code appear in each square unit's description does not matter

## Adding Traffic Lights

Since we with to study traffic control systems, one key element we need in our network models is traffic light. In the current version of the matrix definition, only the centre point of our square (i.e. node `0`) may be assigned with a traffic light, and this is done by simply changing the `p` at the beginning of the square's description to `t`. In the case of our example network, the matrix definition is below if two traffic light controlled juctions are defined at the 3rd and 5th square:

```
p1357 p157 t13578
0 t13574 p1357
```

This updated matrix corresponds to a network represented by the following logo:

{% include svg.html file="matrix_definition_example_2.svg" %}

If the above logo presentation is new to you, then please read our introduction of the network logo format [here](t1_network_logo.html).

## Where to find and/or modify this definition matrix?
A file named `district.matrix` is located in the `data` folder of each one of our network model

<pre>
model_libs
+-- 1x1
|   +-- 01
|   |   +-- data
|   |   |   +-- <b>district.matrix</b>
|   |   |   +-- model.nod.xml
|   |   |   +-- model.edg.xml
|   |   |   +-- model.netccfg
|   |   |   +-- model.net.xml
|   |   |   +-- model.svg
|   |   +-- {Traffic Controller API scripts}
|   +-- 02
|   +-- 03
|   ...
+-- 1x2
+-- 1x3
...
</pre>

## Future Development Directions {#limitations-and-planned-developments}

The proposed Network Definition Matrix sits within the scope of the Traffic Control Test Set project, and it is a key component which resides at the beginning of the Network Construction Workflow. **The priority of this format is to make the network production process simple and user-friendly**. Therefore, all future developments need to comply with this rule.

Current limitations of the format include things such as the eight directions available within each square, and that only one lane is defined at each direction of an edge. As the project progresses, it will become clearer as to which feature is more critical to the project and future developments will be carried out accordingly.


{% include links.html %}
