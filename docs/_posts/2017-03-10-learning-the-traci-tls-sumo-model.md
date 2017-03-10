---
title:  "Learning the TraCI_tls model"
categories: notes
author: Bo Gao
permalink: post-learning-traci-tls.html
tags: [notes, sumo, beginner]
---

## Introduction

TraCI\_tls is a simple SUMO model developed as part of SUMO's tutorial on [TraCI](http://sumo.dlr.de/wiki/TraCI). Depite the tutorial material given [here](http://sumo.dlr.de/wiki/Tutorials/TraCI4Traffic_Lights), I found it difficult to understand the model from a software's point of view. Therefore, I wrote this note to supplement the TraCI\_tls tutorial. Codes related to this model is hosted [here](https://sourceforge.net/p/sumo/code/HEAD/tree/trunk/sumo/tests/complex/tutorial/traci_tls/).

This model has the following file structure:

<pre>
.
+-- data
|   +-- cross.<b>nod</b>.xml 		<b>nodes, junctions</b>
|   +-- cross.<b>edg</b>.xml 		<b>edges, paths, roads</b>
|   +-- [cross.<b>typ</b>.xml] 	<b>edge types</b>
|   +-- cross.<b>con</b>.xml 	<b></b>
|   +-- cross.<b>det</b>.xml 	<b></b>
|   +-- cross.<b>netccfg</b>	<b></b>
|   +-- cross.<b>net</b>.xml 	<b></b>
|   +-- cross.<b>rou</b>.xml 	<b></b>
|   +-- cross.<b>out</b> 		<b>output</b>
|   +-- cross.<b>sumocfg</b>
+-- embedded
|   +-- 
+-- plain
|   +-- 
+-- embedded.py
+-- runner.py 			<b>main script</b>
+-- tripinfo.xml
</pre>

## The `data` folder

This folder contains all "physical assets" of the model. Let's take a look at what's in this folder.

### Nodes and Edges

Nodes and edges are the most basic elements of a SUMO model. Nodes are the reference points on a map, i.e. the "A" and "B" in "Going from A to B". Edges are the paths connecting these reference points.

First, let's look at `cross.nod.xml`:
{% capture text-capture-1 %}

```xml
<?xml version="1.0" encoding="UTF-8"?>
<nodes xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:noNamespaceSchemaLocation="http://sumo.dlr.de/xsd/nodes_file.xsd">
   <node id="0" x="0.0" y="0.0"  type="traffic_light"/>

   <node id="1" x="-500.0" y="0.0" type="priority"/>
   <node id="2" x="+500.0" y="0.0" type="priority"/>
   <node id="3" x="0.0" y="-500.0" type="priority"/>
   <node id="4" x="0.0" y="+500.0" type="priority"/>
   
   <node id="51" x="-510.0" y="0.0" type="priority"/>
   <node id="52" x="+510.0" y="0.0" type="priority"/>
   <node id="53" x="0.0" y="-510.0" type="priority"/>
   <node id="54" x="0.0" y="+510.0" type="priority"/>  
</nodes>
```
{% endcapture %}
{% include custom/toggle-field.html toggle-name="toggle-1" button-text="cross.nod.xml" toggle-text=text-capture-1  footer="" %}

This file defines a list of 9 `node`s, each has a unique `id`, that are "0","1","2","3","4","51","52","53","54". The `x` and `y` locations of each `node` are also given in the definition of each `node`. Each node also has a `type` attribute. Without consulting more documentation, it is easy to understand what "traffic_light" means being `node` 0's type. It must be a junction controlled by traffic lights. But what does `priority` mean for all the other nodes? After consulting [this documentation][1] on SUMO's XML schema, it appeared that this is related to the `priority` attribute of `edge`s, so let's take a look at our next file `cross.edg.xml`:

{% capture text-capture-2 %}

```xml
<?xml version="1.0" encoding="UTF-8"?>
<edges xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:noNamespaceSchemaLocation="http://sumo.dlr.de/xsd/edges_file.xsd">
   <edge id="1i" from="1" to="0" priority="78" numLanes="1" speed="19.444" />
   <edge id="1o" from="0" to="1" priority="46" numLanes="1" speed="11.111" />

   <edge id="2i" from="2" to="0" priority="78" numLanes="1" speed="19.444" />
   <edge id="2o" from="0" to="2" priority="46" numLanes="1" speed="11.111" />

   <edge id="3i" from="3" to="0" priority="78" numLanes="1" speed="19.444" />
   <edge id="3o" from="0" to="3" priority="46" numLanes="1" speed="11.111" />
	...

</edges>
```
{% endcapture %}
{% include custom/toggle-field.html toggle-name="toggle-2" button-text="cross.edg.xml" toggle-text=text-capture-2  footer="" %}

From this file we have definition of a bunch of `edge`s, each again has a unique `id` such as "1i" for the edge going `from` `node` "1" `to` `node` "0". To answer our earlier question regarding the `priority` typed `node`s, we see that each `edge` has a `priority` attribute which has numerical values meaning that `edge`s can be compared according to their `priority`s. In this model, edges going into the juction (node 0), i.e. "\*i" edges, have a higher priority of 78 than those exiting the junction, i.e. "\*o" edges which have a lower priority of 46. <i class="fa fa-stethoscope"></i>

Apart from `priority`, we also have `numLanes` and `speed` as attributes for `edge`s. These are easy to understand literally. But this file has lots of repetitive codes, and this is not ideal from a programming point of view. Not to worry though, SUMO has this covered with a `*.typ.xml` file which we will take a look at in the next section.

Before we finish this section, let's quickly summarise what we know about the definitions of nodes and edges so far of TraCI_tls with this illustration:

![Illustration: Nodes and Edges](https://intelaligent.github.io/tctester/images/learn_traci_1.svg)

**Further readings**: On `node` types (extract from [here][1]:):
{% capture text-capture-3 %}

 - `priority`: Vehicles on a low-priority edge have to wait until vehicles on a high-priority edge have passed the junction.
 - `traffic_light`: The junction is controlled by a traffic light (priority rules are used to avoid collisions if conflicting links have green  - light at the same time).
 - `right_before_left`: Vehicles will let vehicles coming from their right side pass.
 - `unregulated`: The junction is completely unregulated - all vehicles may pass without braking; this may cause collisions
 - `traffic_light_unregulated`: The junction is controlled by a traffic light without any further rules. this may cause collision if unsafe signal  - plans are used
 - `priority_stop`: This works like a priority-junction but vehicles on minor links alway have to stop before passing
 - `allway_stop`: This junction works like an [All-way stop]
 - `rail_signal`: This junction is controlled by a rail signal. This type of junction/control is only useful for rails.
 - `zipper`: This junction connects edges where the number of lanes decreases and traffic needs to merge zipper-style (late merging).
 - `rail_crossing`: This junction models a rail road crossing. It will allow trains to pass unimpeded and will restrict vehicles via traffic  - signals when a train is approaching..
 - `traffic_light_right_on_red`: The junction is controlled by a traffic light as for type traffic_light. Additionally, right-turning vehicles may drive in any phase whenever it is safe to do so (after stopping once). This behavior is known as right-turn-on-red.
{% endcapture %}
{% include custom/toggle-field.html toggle-name="toggle-3" button-text="all possible node types" toggle-text=text-capture-3  footer="" %}

### Define edge types with a `*.typ.xml` file

Indeed, there is no `cross.typ.xml` file included in this model, but there could have been one and it would have looked like this:

{% capture text-capture-4 %}

```xml
<?xml version="1.0" encoding="UTF-8"?>
<types>
   <type id="go_in_to_junction" priority="78" numLanes="1" speed="19.444"/>
   <type id="come_out_of_junction" priority="46" numLanes="1" speed="11.111"/>
</types>
```
{% endcapture %}
{% include custom/toggle-field.html toggle-name="toggle-4" button-text="cross.typ.xml" toggle-text=text-capture-4  footer="" %}

With the addition of this `cross.typ.xml` file, the `cross.edg.xml` file can be simplified as:

{% capture text-capture-5 %}

```xml
<?xml version="1.0" encoding="UTF-8"?>
<edges xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:noNamespaceSchemaLocation="http://sumo.dlr.de/xsd/edges_file.xsd">
   <edge id="1i" from="1" to="0" type="go_in_to_junction" />
   <edge id="1o" from="0" to="1" type="come_out_of_junction" />

   <edge id="2i" from="2" to="0" type="go_in_to_junction" />
   <edge id="2o" from="0" to="2" type="come_out_of_junction" />

   <edge id="3i" from="3" to="0" type="go_in_to_junction" />
   <edge id="3o" from="0" to="3" type="come_out_of_junction" />
	...

</edges>
```
{% endcapture %}
{% include custom/toggle-field.html toggle-name="toggle-5" button-text="modified cross.edg.xml" toggle-text=text-capture-5  footer="" %}

Compare this to the original version:

{% include custom/toggle-field.html toggle-name="toggle-6" button-text="original cross.edg.xml" toggle-text=text-capture-2  footer="" %}

You can see that `edge` attributes such as `priority` and `numLanes` have been extracted and grouped together in the `cross.typ.xml` file. This is useful when you have many edges of the same type, and it is also a good practice from a programming point of view.

**Further reading**: To get a full list of the attributes an `edge` may have, consult SUMO's documentation on its `*.typ.xml` file [here](http://sumo.dlr.de/wiki/SUMO_edge_type_file).

### Connect edges with a `*.con.xml` file

We now have 8 edges all associated with `node` 0, a `traffic_light` typed `node`. These edges have yet to be connected together, i.e. rules are yet to be defined to route vehicles from one edge to another. Let's see how this is done in TraCI_tls:

{% capture text-capture-7 %}

```xml
<?xml version="1.0" encoding="iso-8859-1"?>
<connections xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:noNamespaceSchemaLocation="http://sumo.dlr.de/xsd/connections_file.xsd">
	<connection from="1i" to="2o"/>
	<connection from="2i" to="1o"/>
	<connection from="3i" to="4o"/>
	<connection from="4i" to="3o"/>
</connections>
```
{% endcapture %}
{% include custom/toggle-field.html toggle-name="toggle-7" button-text="cross.con.xml" toggle-text=text-capture-7  footer="" %}

![Illustration: Connections](https://intelaligent.github.io/tctester/images/learn_traci_2.svg)


[1]: http://sumo.dlr.de/wiki/Networks/Building_Networks_from_own_XML-descriptions "XML descriptions"

{% include links.html %}