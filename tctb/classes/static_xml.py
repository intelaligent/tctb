def gui_settings():
    return """<viewsettings>
    <delay value="100"/>
    <scheme name="custom_district">
        <vehicles vehicleMode="8" />
    </scheme>
</viewsettings>
"""

def vTypes_file():
    return """<?xml version="1.0"?>
<additional>
    <vType id="tctb_default" maxSpeed="40.2" length="5" accel="2.6" decel="4.5" sigma="0.5" tau="1.0"/>
</additional>
"""

def dump_file(work_dir):
    return """<?xml version="1.0"?>
<additional>
    <edgeData id="edge_dump" file="out_dumps_edge.xml" excludeEmpty="true"/>
    <edgeData id="edge_dump_emissions" type="emissions" file="out_dumps_emissions_edge.xml" excludeEmpty="true"/>
    <laneData id="lane_dump" file="out_dumps_lane.xml"/>
</additional>
"""