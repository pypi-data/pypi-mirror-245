"""
  scenariogeneration
  https://github.com/pyoscx/scenariogeneration

  This Source Code Form is subject to the terms of the Mozilla Public
  License, v. 2.0. If a copy of the MPL was not distributed with this
  file, You can obtain one at https://mozilla.org/MPL/2.0/.

  Copyright (c) 2022 The scenariogeneration Authors.

"""
from scenariogeneration.xodr.opendrive import OpenDrive
import pytest
from scenariogeneration import xodr as pyodrx
from scenariogeneration import prettyprint
from .xml_validator import version_validation, ValidationResponse


def test_simple_road():
    line1 = pyodrx.Line(100)
    planview = pyodrx.PlanView()
    planview.add_geometry(line1)

    rm = pyodrx.RoadMark(
        pyodrx.RoadMarkType.solid, 0.2, rule=pyodrx.MarkRule.no_passing
    )

    lane1 = pyodrx.Lane(a=2)
    lane1.add_roadmark(rm)
    lanesec = pyodrx.LaneSection(0, lane1)

    lanes = pyodrx.Lanes()
    lanes.add_lanesection(lanesec)

    road = pyodrx.Road(1, planview, lanes)
    road.planview.adjust_geometries()

    prettyprint(road.get_element())
    assert (
        version_validation("t_road", road, wanted_schema="xodr")
        == ValidationResponse.OK
    )


def test_link_road():
    planview = pyodrx.PlanView()
    planview.add_geometry(pyodrx.Line(100))
    lane1 = pyodrx.Lane(a=2)
    lane1.add_roadmark(
        pyodrx.RoadMark(pyodrx.RoadMarkType.solid, 0.2, rule=pyodrx.MarkRule.no_passing)
    )
    lanes = pyodrx.Lanes()
    lanes.add_lanesection(pyodrx.LaneSection(0, lane1))

    road = pyodrx.Road(1, planview, lanes)
    road.add_predecessor(pyodrx.ElementType.road, "1", pyodrx.ContactPoint.start)
    prettyprint(road.get_element())

    planview2 = pyodrx.PlanView()
    planview2.add_geometry(pyodrx.Line(100))
    lane12 = pyodrx.Lane(a=2)
    lane12.add_roadmark(
        pyodrx.RoadMark(pyodrx.RoadMarkType.solid, 0.2, rule=pyodrx.MarkRule.no_passing)
    )
    lanes2 = pyodrx.Lanes()
    lanes2.add_lanesection(pyodrx.LaneSection(0, lane12))

    road2 = pyodrx.Road(1, planview2, lanes2)
    road2.add_predecessor(pyodrx.ElementType.road, "1", pyodrx.ContactPoint.start)

    planview3 = pyodrx.PlanView()
    planview3.add_geometry(pyodrx.Line(120))
    lane13 = pyodrx.Lane(a=2)
    lane13.add_roadmark(
        pyodrx.RoadMark(pyodrx.RoadMarkType.solid, 0.2, rule=pyodrx.MarkRule.no_passing)
    )
    lanes3 = pyodrx.Lanes()
    lanes3.add_lanesection(pyodrx.LaneSection(0, lane13))

    road3 = pyodrx.Road(2, planview3, lanes3)
    road3.add_predecessor(pyodrx.ElementType.road, "1", pyodrx.ContactPoint.start)

    odr = pyodrx.OpenDrive("")
    odr2 = pyodrx.OpenDrive("")
    odr3 = pyodrx.OpenDrive("")
    odr.add_road(road)
    odr2.add_road(road2)
    odr3.add_road(road3)
    odr.adjust_roads_and_lanes()
    odr2.adjust_roads_and_lanes()
    odr3.adjust_roads_and_lanes()

    assert odr == odr2
    assert odr != odr3
    assert version_validation(None, odr, wanted_schema="xodr") == ValidationResponse.OK


@pytest.mark.parametrize(
    "data",
    [
        ([10, 100, -1, 1, 3]),
        ([10, 50, -1, 1, 3]),
        ([10, 100, 1, 1, 3]),
        ([10, 100, -1, 2, 3]),
        ([10, 100, -1, 10, 3]),
        ([10, 100, -1, 10, 5]),
    ],
)
def test_create_straight_road(data):
    road = pyodrx.generators.create_straight_road(
        data[0], length=data[1], junction=data[2], n_lanes=data[3], lane_offset=data[4]
    )
    odr = pyodrx.OpenDrive("myroad")
    odr.add_road(road)
    odr.adjust_roads_and_lanes()

    redict = road.get_attributes()

    assert int(redict["id"]) == data[0]
    assert int(redict["length"]) == data[1]
    assert int(redict["junction"]) == data[2]
    assert len(road.lanes.lanesections[0].leftlanes) == data[3]
    assert len(road.lanes.lanesections[0].rightlanes) == data[3]
    assert road.lanes.lanesections[0].leftlanes[0].widths[0].a == data[4]
    assert road.lanes.lanesections[0].leftlanes[0].widths[0].b == 0
    assert road.lanes.lanesections[0].leftlanes[0].widths[0].c == 0
    assert road.lanes.lanesections[0].leftlanes[0].widths[0].d == 0
    assert version_validation(None, odr, wanted_schema="xodr") == ValidationResponse.OK


def test_road_type():
    rt = pyodrx.opendrive._Type(pyodrx.RoadType.motorway, 0, "SE")
    prettyprint(rt.get_element())
    rt2 = pyodrx.opendrive._Type(pyodrx.RoadType.motorway, 0, "SE")
    rt3 = pyodrx.opendrive._Type(pyodrx.RoadType.motorway, 0, "DE")
    assert rt == rt2
    assert rt != rt3

    rt = pyodrx.opendrive._Type(pyodrx.RoadType.motorway, 0, "SE", speed="no limit")
    prettyprint(rt.get_element())
    rt2 = pyodrx.opendrive._Type(pyodrx.RoadType.motorway, 0, "SE", speed="no limit")
    rt3 = pyodrx.opendrive._Type(pyodrx.RoadType.motorway, 1, "SE", speed="no limit")
    assert rt == rt2
    assert rt != rt3
    assert (
        version_validation("t_road_type", rt, wanted_schema="xodr")
        == ValidationResponse.OK
    )


def test_road_with_road_types():
    road = pyodrx.create_straight_road(0)
    road.add_type(pyodrx.RoadType.motorway, 0)
    prettyprint(road.get_element())

    road2 = pyodrx.create_straight_road(0)
    road2.add_type(pyodrx.RoadType.motorway, 0)
    road3 = pyodrx.create_straight_road(0, 50)
    road3.add_type(pyodrx.RoadType.motorway, 0)

    odr = pyodrx.OpenDrive("")
    odr2 = pyodrx.OpenDrive("")
    odr3 = pyodrx.OpenDrive("")
    odr.add_road(road)
    odr2.add_road(road2)
    odr3.add_road(road3)
    odr.adjust_roads_and_lanes()
    odr2.adjust_roads_and_lanes()
    odr3.adjust_roads_and_lanes()

    assert road == road2
    assert road.planview != road3.planview
    assert odr == odr2
    assert odr != odr3
    assert version_validation(None, odr, wanted_schema="xodr") == ValidationResponse.OK


def test_road_with_repeating_objects():
    r1 = pyodrx.create_straight_road(0)
    r2 = pyodrx.create_straight_road(0)
    r3 = pyodrx.create_straight_road(0)
    guardrail = pyodrx.Object(
        0, 0, height=2.0, zOffset=0, Type=pyodrx.ObjectType.barrier, name="railing"
    )
    odr = pyodrx.OpenDrive("")
    odr2 = pyodrx.OpenDrive("")
    odr3 = pyodrx.OpenDrive("")
    odr.add_road(r1)
    odr2.add_road(r2)
    odr3.add_road(r3)
    odr.adjust_roads_and_lanes()
    odr2.adjust_roads_and_lanes()
    odr3.adjust_roads_and_lanes()
    r3.add_object_roadside(guardrail, 4, 0, 0, pyodrx.RoadSide.both, 1, 0.1, 4, 1, 4, 1)
    prettyprint(odr3.get_element())

    assert r1 == r2
    assert r1 != r3
    assert odr == odr2
    assert odr != odr3
    assert version_validation(None, odr, wanted_schema="xodr") == ValidationResponse.OK


def test_header():
    h1 = pyodrx.opendrive._Header("hej", "1", "4")
    h2 = pyodrx.opendrive._Header("hej", "1", "4")
    h3 = pyodrx.opendrive._Header("hej", "1", "5")
    assert h1 == h2
    assert h1 != h3
    assert (
        version_validation("t_header", h1, wanted_schema="xodr")
        == ValidationResponse.OK
    )
