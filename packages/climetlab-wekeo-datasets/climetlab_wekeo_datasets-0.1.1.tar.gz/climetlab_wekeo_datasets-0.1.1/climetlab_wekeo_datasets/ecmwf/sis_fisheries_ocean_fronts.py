#!/usr/bin/env python3
# (C) Copyright 2023 European Centre for Medium-Range Weather Forecasts.
# This software is licensed under the terms of the Apache Licence Version 2.0
# which can be obtained at http://www.apache.org/licenses/LICENSE-2.0.
# In applying this licence, ECMWF does not waive the privileges and immunities
# granted to it by virtue of its status as an intergovernmental organisation
# nor does it submit to any jurisdiction.
from __future__ import annotations

from climetlab.decorators import normalize

from climetlab_wekeo_datasets.ecmwf.main import Main


class sis_fisheries_ocean_fronts(Main):
    name = "EO:ECMWF:DAT:SIS_FISHERIES_OCEAN_FRONTS"
    dataset = "EO:ECMWF:DAT:SIS_FISHERIES_OCEAN_FRONTS"

    choices = [
        "format_",
    ]

    string_selects = [
        "experiment",
        "indicator",
        "month",
        "origin",
        "variable",
        "year",
    ]

    @normalize(
        "experiment",
        [
            "rcp4_5",
            "rcp8_5",
        ],
        multiple=True,
    )
    @normalize(
        "indicator",
        [
            "chlorophyll_a_density",
            "sea_surface_temperature",
        ],
        multiple=True,
    )
    @normalize(
        "month",
        [
            "01",
            "02",
            "03",
            "04",
            "05",
            "06",
            "07",
            "08",
            "09",
            "10",
            "11",
            "12",
        ],
        multiple=True,
    )
    @normalize(
        "origin",
        [
            "nemo_ersem",
            "polcoms_cci",
            "polcoms_ersem",
        ],
        multiple=True,
    )
    @normalize(
        "variable",
        [
            "change_in_distance_to_nearest_major_front",
            "change_in_frontal_gradient_magnitude",
            "change_in_frontal_persistence",
            "distance_to_nearest_major_front",
            "frontal_gradient_magnitude",
            "frontal_persistence",
        ],
        multiple=True,
    )
    @normalize(
        "year",
        [
            "1991",
            "1992",
            "1993",
            "1994",
            "1995",
            "1996",
            "1997",
            "1998",
            "1999",
            "2000",
            "2001",
            "2002",
            "2003",
            "2004",
            "2005",
            "2006",
            "2007",
            "2008",
            "2009",
            "2010",
            "2011",
            "2012",
            "2013",
            "2014",
            "2015",
            "2016",
            "2017",
            "2018",
            "2019",
            "2020",
            "2021",
            "2022",
            "2023",
            "2024",
            "2025",
            "2026",
            "2027",
            "2028",
            "2029",
            "2030",
            "2031",
            "2032",
            "2033",
            "2034",
            "2035",
            "2036",
            "2037",
            "2038",
            "2039",
            "2040",
            "2041",
            "2042",
            "2043",
            "2044",
            "2045",
            "2046",
            "2047",
            "2048",
            "2049",
            "2050",
            "2051",
            "2052",
            "2053",
            "2054",
            "2055",
            "2056",
            "2057",
            "2058",
            "2059",
            "2060",
            "2061",
            "2062",
            "2063",
            "2064",
            "2065",
            "2066",
            "2067",
            "2068",
            "2069",
            "2070",
            "2071",
            "2072",
            "2073",
            "2074",
            "2075",
            "2076",
            "2077",
            "2078",
            "2079",
            "2080",
            "2081",
            "2082",
            "2083",
            "2084",
            "2085",
            "2086",
            "2087",
            "2088",
            "2089",
            "2090",
            "2091",
            "2092",
            "2093",
            "2094",
            "2095",
            "2096",
            "2097",
            "2098",
            "2099",
        ],
        multiple=True,
    )
    @normalize(
        "format_",
        [
            "tgz",
            "zip",
        ],
    )
    def __init__(
        self,
        experiment,
        indicator,
        month,
        origin,
        variable,
        year,
        format_=None,
    ):
        super().__init__(
            experiment=experiment,
            indicator=indicator,
            month=month,
            origin=origin,
            variable=variable,
            year=year,
            format_=format_,
        )
