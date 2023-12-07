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
    "cmems_obs-wind_glo_phy_my_l4_P1M_202211",  # noqa: E501  global ocean - wind and stress - monthly - from scatterometer and model
]


class wind_glo_phy_climate_l4_my(Main):
    name = "EO:MO:DAT:WIND_GLO_PHY_CLIMATE_L4_MY_012_003"
    dataset = "EO:MO:DAT:WIND_GLO_PHY_CLIMATE_L4_MY_012_003"

    string_selects = [
        "variables",
    ]

    @normalize("layer", LAYERS)
    @normalize("area", "bounding-box(list)")
    @normalize(
        "variables",
        [
            "eastward_stress",
            "eastward_stress_bias",
            "eastward_stress_sdd",
            "eastward_wind",
            "eastward_wind_bias",
            "eastward_wind_sdd",
            "lat",
            "lon",
            "northward_stress",
            "northward_stress_bias",
            "northward_stress_sdd",
            "northward_wind",
            "northward_wind_bias",
            "northward_wind_sdd",
            "number_of_observations",
            "time",
        ],
        multiple=True,
    )
    @normalize("start", "date(%Y-%m-%dT%H:%M:%SZ)")
    @normalize("end", "date(%Y-%m-%dT%H:%M:%SZ)")
    def __init__(
        self,
        layer="cmems_obs-wind_glo_phy_my_l4_P1M_202211",
        area=None,
        variables=None,
        start=None,
        end=None,
    ):
        if layer == "cmems_obs-wind_glo_phy_my_l4_P1M_202211":
            if start is None:
                start = "1999-08-01T00:00:00Z"

            if end is None:
                end = "2023-06-30T23:59:59Z"

        super().__init__(
            layer=layer,
            area=area,
            variables=variables,
            start=start,
            end=end,
        )
