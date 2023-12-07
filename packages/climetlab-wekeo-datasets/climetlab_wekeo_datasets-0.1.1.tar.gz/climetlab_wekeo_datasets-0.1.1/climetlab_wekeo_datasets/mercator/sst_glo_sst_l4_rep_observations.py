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
    "METOFFICE-GLO-SST-L4-REP-OBS-SST_202003",  # noqa: E501 Global sst & sea ice analysis, l4 ostia, 0.05 deg daily (metoffice-glo-sst-l4-rep-obs-sst-v2)
]


class sst_glo_sst_l4_rep_observations(Main):
    name = "EO:MO:DAT:SST_GLO_SST_L4_REP_OBSERVATIONS_010_011"
    dataset = "EO:MO:DAT:SST_GLO_SST_L4_REP_OBSERVATIONS_010_011"

    string_selects = [
        "variables",
    ]

    @normalize("layer", LAYERS)
    @normalize("area", "bounding-box(list)")
    @normalize(
        "variables",
        [
            "analysed_sst",
            "analysis_error",
            "lat",
            "lon",
            "mask",
            "sea_ice_fraction",
            "time",
        ],
        multiple=True,
    )
    @normalize("start", "date(%Y-%m-%dT%H:%M:%SZ)")
    @normalize("end", "date(%Y-%m-%dT%H:%M:%SZ)")
    def __init__(
        self,
        layer="METOFFICE-GLO-SST-L4-REP-OBS-SST_202003",
        area=None,
        variables=None,
        start=None,
        end=None,
    ):
        if layer == "METOFFICE-GLO-SST-L4-REP-OBS-SST_202003":
            if start is None:
                start = "1981-10-01T00:00:00Z"

            if end is None:
                end = "2022-06-01T00:00:00Z"

        super().__init__(
            layer=layer,
            area=area,
            variables=variables,
            start=start,
            end=end,
        )
