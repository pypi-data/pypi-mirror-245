#!/usr/bin/env python3
# (C) Copyright 2023 European Centre for Medium-Range Weather Forecasts.
# This software is licensed under the terms of the Apache Licence Version 2.0
# which can be obtained at http://www.apache.org/licenses/LICENSE-2.0.
# In applying this licence, ECMWF does not waive the privileges and immunities
# granted to it by virtue of its status as an intergovernmental organisation
# nor does it submit to any jurisdiction.
from __future__ import annotations

from climetlab.decorators import normalize

from climetlab_wekeo_datasets.mercator.main import Main

LAYERS = [
    "cmems_mod_arc_bgc_my_ecosmo_P1D-m_202105",  # noqa: E501 Arctic ocean biogeochemistry reanalysis, 25km surface daily mean
    "cmems_mod_arc_bgc_my_ecosmo_P1M_202105",  # noqa: E501 Arctic ocean biogeochemistry reanalysis, 25km monthly mean
    "cmems_mod_arc_bgc_my_ecosmo_P1Y_202211",  # noqa: E501 Arctic ocean biogeochemistry reanalysis, 25km yearly mean
]


class arctic_multiyear_bgc(Main):
    name = "EO:MO:DAT:ARCTIC_MULTIYEAR_BGC_002_005"
    dataset = "EO:MO:DAT:ARCTIC_MULTIYEAR_BGC_002_005"

    string_selects = [
        "variables",
    ]

    @normalize("layer", LAYERS)
    @normalize("area", "bounding-box(list)")
    @normalize(
        "variables",
        [
            "chl",
            "depth",
            "kd",
            "latitude",
            "longitude",
            "model_depth",
            "no3",
            "nppv",
            "o2",
            "phyc",
            "po4",
            "si",
            "stereographic",
            "time",
            "x",
            "y",
            "zooc",
        ],
        multiple=True,
    )
    @normalize("start", "date(%Y-%m-%dT%H:%M:%SZ)")
    @normalize("end", "date(%Y-%m-%dT%H:%M:%SZ)")
    def __init__(
        self,
        layer,
        area=None,
        variables=None,
        start=None,
        end=None,
    ):
        if layer == "cmems_mod_arc_bgc_my_ecosmo_P1D-m_202105":
            if start is None:
                start = "2007-01-01T00:00:00Z"

            if end is None:
                end = "2020-12-31T00:00:00Z"

        if layer == "cmems_mod_arc_bgc_my_ecosmo_P1M_202105":
            if start is None:
                start = "2007-01-15T00:00:00Z"

            if end is None:
                end = "2020-12-15T00:00:00Z"

        if layer == "cmems_mod_arc_bgc_my_ecosmo_P1Y_202211":
            if start is None:
                start = "2007-01-01T00:00:00Z"

            if end is None:
                end = "2020-01-01T00:00:00Z"

        super().__init__(
            layer=layer,
            area=area,
            variables=variables,
            start=start,
            end=end,
        )
