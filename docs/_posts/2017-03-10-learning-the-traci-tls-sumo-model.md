---
title:  "Learning the TraCI_tls model"
categories: notes
author: Bo Gao
permalink: post-learning-traci-tls.html
tags: [notes]
---

## Introduction

TraCI\_tls is a simple SUMO model developed as part of SUMO's tutorial on [TraCI](http://sumo.dlr.de/wiki/TraCI). Depite the tutorial material given [here](http://sumo.dlr.de/wiki/Tutorials/TraCI4Traffic_Lights), I found it difficult to understand the model from a software's point of view. Therefore, I wrote this note to supplement the TraCI\_tls tutorial. Codes related to this model is hosted [here](https://sourceforge.net/p/sumo/code/HEAD/tree/trunk/sumo/tests/complex/tutorial/traci_tls/).

This model has the following file structure:

<pre>
.
+-- data
|   +-- cross.<b>nod</b>.xml 	<b>nodes, junctions</b>
|   +-- cross.<b>edg</b>.xml 	<b>edges, paths, roads</b>
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

This folder contains all "physical assets" of the model. Let's take a look at what's in this folder

### Nodes and Edges

Nodes and edges are the most basic elements of a SUMO model. Nodes are the reference points on a map, i.e. the "A" and "B" in "Going from A to B". Edges are the paths connecting these reference points.


cross.**nod**.xml
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

cross.**edg**.xml
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

To illustrate, we now have:

![Illustration 1](https://intelaligent.github.io/tctester/images/learn_traci_1.png)


I found [this document][1] to be useful to understand the XML 

[1]: http://sumo.dlr.de/wiki/Networks/Building_Networks_from_own_XML-descriptions "XML descriptions"
