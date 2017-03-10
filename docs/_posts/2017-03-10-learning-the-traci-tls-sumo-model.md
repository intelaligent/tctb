---
title:  "Learning the TraCI_tls model"
categories: notes
author: Bo Gao
permalink: post-learning-traci-tls.html
tags: [notes, sumo, beginner]
---

## Introduction

TraCI\_tls is a simple SUMO model developed as part of SUMO's tutorial on [TraCI](http://sumo.dlr.de/wiki/TraCI). Depite the tutorial material given [here](http://sumo.dlr.de/wiki/Tutorials/TraCI4Traffic_Lights), I found it difficult to understand the model from a software's point of view. Also making connections between SUMO's wiki is also not a simple task. Therefore, I wrote this study note to supplement the TraCI\_tls tutorial. Codes related to this model is hosted [here](https://sourceforge.net/p/sumo/code/HEAD/tree/trunk/sumo/tests/complex/tutorial/traci_tls/).

First let's take a look at the file structure of TraCI\_tls:

<pre>
.
+-- data
|   +-- cross.<b>nod</b>.xml 		<b>nodes, junctions</b>
|   +-- cross.<b>edg</b>.xml 		<b>edges, paths, roads</b>
|   +-- [cross.<b>typ</b>.xml] 	<b>edge types</b>
|   +-- cross.<b>con</b>.xml 	<b></b>
|   +-- cross.<b>netccfg</b>	<b></b>
|   +-- cross.<b>net</b>.xml 	<b></b>
|   +-- cross.<b>det</b>.xml 	<b></b>
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

**Further reading**: On `node` types (extract from [here][1]:):
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

The code for `connection`s are self-explanatory with `from` and `to` to establish a link between two edges which we illustrate below:
![Illustration: Connections](https://intelaligent.github.io/tctester/images/learn_traci_2.svg)

Indeed, `from` and `to` are the most essential attributes of a `connection`. Other attributes are also available for defining a connection:

{% capture text-capture-8 %}
| Attribute | Description |
|-------|-------|
| fromLane | \<int\>, the lane index of the incoming lane (numbers starting with 0) |
| toLane | \<int\>, the lane index of the outgoing lane (numbers starting with 0) |
| pass | \<bool\>, if set, vehicles which pass this (lane-2-lane) connection) will not wait |
| keepClear | \<bool\>, if set to false, vehicles which pass this (lane-2-lane) connection) will not worry about blocking the intersection. |
| contPos | \<float\>, if set to 0, no internal junction will be built for this connection. If set to a positive value, an internal junction will be built at this position (in m) from the start of the internal lane for this connection. |
| visibility | \<float\>, specifies the distance to the connection [in m.] below which an approaching vehicle has full sight of any other approaching vehicles on the connection's foe lanes (i.e. vehicle can accelerate if none are present). Defaults to 4.5m. Note that a too low visibility (\<=0.1m.) will prevent vehicles from crossing a minor link. For major links the attribute has no effect, currently. |
| uncontrolled | \<bool\>, if set to true, This connection will not be TLS-controlled despite its node being controlled. |
{% endcapture %}
{% include custom/toggle-field.html toggle-name="toggle-8" button-text="connection attributes" toggle-text=text-capture-8  footer="" %}

According to these attributes, there are a lot you can do with a `connection`, but let's concentrate on TraCI_tls for now.

**Further reading** on `connection`s is available [here](http://sumo.dlr.de/wiki/Networks/Building_Networks_from_own_XML-descriptions#Connection_Descriptions) .

### Generate `*.net.xml`, with `netconvert` and `*.netccfg`

Before we dive deeper in the `data` folder, let's take a look at what assets we have got so far for the TraCI_tls model:
<pre>
.
+-- data
|   +-- <i class="fa fa-check-square"> </i>cross.<b>nod</b>.xml 		<b>nodes, junctions</b>
|   +-- <i class="fa fa-check-square"> </i>cross.<b>edg</b>.xml 		<b>edges, paths, roads</b>
|   +-- <i class="fa fa-check-square"> </i>[cross.<b>typ</b>.xml] 		<b>edge types</b>
|   +-- <i class="fa fa-check-square"> </i>cross.<b>con</b>.xml			<b>connection between edges</b>
|   +-- <i class="fa fa-square"> </i>cross.<b>netccfg</b>
|   +-- <i class="fa fa-square"> </i>cross.<b>net</b>.xml
|   +-- <i class="fa fa-square"> </i>cross.<b>det</b>.xml
|   +-- <i class="fa fa-square"> </i>cross.<b>rou</b>.xml
|   +-- <i class="fa fa-square"> </i>cross.<b>out</b>
|   +-- <i class="fa fa-square"> </i>cross.<b>sumocfg</b>
...
</pre>
With the 4 checked files, we are now ready to put the `node`s, `edge`s, and `connection`s together to construct a complete "network". In order to do this, first we need to write a network configuration file named `cross.netccfg`:

{% capture text-capture-9 %}
```xml
<?xml version="1.0" encoding="UTF-8"?>

<configuration xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:noNamespaceSchemaLocation="http://sumo.dlr.de/xsd/netconvertConfiguration.xsd">

    <input>
        <node-files value="cross.nod.xml"/>
        <edge-files value="cross.edg.xml"/>
        <connection-files value="cross.con.xml"/>
    </input>

    <output>
        <output-file value="cross.net.xml"/>
    </output>

    <report>
        <verbose value="true"/>
    </report>

</configuration>
```
{% endcapture %}
{% include custom/toggle-field.html toggle-name="toggle-9" button-text="cross.netccfg" toggle-text=text-capture-9  footer="" %}

{% include tip.html content="Note that both `cross.netccfg` and `cross.netc.cfg` are acceptable suffixes to SUMO's GUI. If you are not using the GUI then this file can have any name as long as you give it correctly to `netconvert`." %}

`cross.netccfg` is very literal with `input` and `output` files specified in the first two sections. The `verbose` option in the `report` section controls the verbose output behaviour of `netconvert`.

On a command line, execute the following command to generate a `cross.net.xml` file.

```
netconvert -c cross.netccfg
```

`netconvert` is a SUMO binary just like `sumo` and `sumo-gui`. If you compiled SUMO from source then this together with all other SUMO binaries should be in your `bin` folder, for example in my case this is the `~/sumo-0.29.0/bin/` folder. If you `make install`-ed, then these binaries will be located somewhere like `/usr/local/bin/`. Issue a `which netconvert` command to find out where it is.

{% include tip.html content="The purpose of the `cross.netccfg` file is to make calling `netconvert` earlier for the user. Without `cross.netccfg`, an equivalent result can be achieved by executing 
<br/><br/>```netconvert -n cross.nod.xml -e cross.nod.xml -x cross.con.xml -o cross.net.xml```<br/><br/>
on command line." %}

**Further reading** on `netconvert` is available [here](http://sumo.dlr.de/wiki/NETCONVERT).

### Network Summary

Let's summarise the process of generating a network with the following illustration:

![Illustration: Network Summary](https://intelaligent.github.io/tctester/images/learn_traci_b_1.svg)

Our progress through the `data` folder looks like this:
<pre>
.
+-- data
|   +-- <i class="fa fa-check-square"> </i>cross.<b>nod</b>.xml 		<b>nodes, junctions</b>
|   +-- <i class="fa fa-check-square"> </i>cross.<b>edg</b>.xml 		<b>edges, paths, roads</b>
|   +-- <i class="fa fa-check-square"> </i>[cross.<b>typ</b>.xml] 		<b>edge types</b>
|   +-- <i class="fa fa-check-square"> </i>cross.<b>con</b>.xml			<b>connection between edges</b>
|   +-- <i class="fa fa-check-square"> </i>cross.<b>netccfg</b>			<b>network configuration</b>
|   +-- <i class="fa fa-check-square"> </i>cross.<b>net</b>.xml 		<b>network</b>
|   +-- <i class="fa fa-square"> </i>cross.<b>det</b>.xml
|   +-- <i class="fa fa-square"> </i>cross.<b>rou</b>.xml
|   +-- <i class="fa fa-square"> </i>cross.<b>out</b>
|   +-- <i class="fa fa-square"> </i>cross.<b>sumocfg</b>
...
</pre>

### On the road with `*.rou.xml`


### Equip the road with `*.det.xml`


### Start the simulation with SUMO


### Simulation Summary
![Illustration: Network Summary](https://intelaligent.github.io/tctester/images/learn_traci_b_2.svg)

[detectors](http://sumo.dlr.de/wiki/Simulation/Output/Induction_Loops_Detectors_(E1))

[detectors TraCI](http://sumo.dlr.de/wiki/TraCI/Induction_Loop_Value_Retrieval)

[additional files](http://sumo.dlr.de/wiki/SUMO#Format_of_additional_files)


I'm still writing...

[1]: http://sumo.dlr.de/wiki/Networks/Building_Networks_from_own_XML-descriptions "XML descriptions"

{% include links.html %}