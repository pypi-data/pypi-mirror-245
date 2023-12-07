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
    "cmems_obs_oc_med_bgc_geophy_nrt_l3-hr_P1D-m_202105",  # noqa: E501 cmems_obs_oc_med_bgc_geophy_nrt_l3-hr_P1D-m_202105
    "cmems_obs_oc_med_bgc_optics_nrt_l3-hr_P1D-m_202105",  # noqa: E501 cmems_obs_oc_med_bgc_optics_nrt_l3-hr_P1D-m_202105
    "cmems_obs_oc_med_bgc_transp_nrt_l3-hr_P1D-m_202105",  # noqa: E501 cmems_obs_oc_med_bgc_transp_nrt_l3-hr_P1D-m_202105
    "cmems_obs_oc_med_bgc_tur-spm-chl_nrt_l3-hr-mosaic_P1D-m_202107",  # noqa: E501 Cmems hr-oc mediterranean sea transparency (spm, tur) and geophysical (chl) daily observations mosaic
]


class oceancolour_med_bgc_hr_l3_nrt(Main):
    name = "EO:MO:DAT:OCEANCOLOUR_MED_BGC_HR_L3_NRT_009_205"
    dataset = "EO:MO:DAT:OCEANCOLOUR_MED_BGC_HR_L3_NRT_009_205"

    string_selects = [
        "variables",
    ]

    @normalize("layer", LAYERS)
    @normalize("area", "bounding-box(list)")
    @normalize(
        "variables",
        [
            "BBP443",
            "BBP492",
            "BBP560",
            "BBP665",
            "BBP704",
            "BBP740",
            "BBP783",
            "BBP865",
            "CHL",
            "RRS443",
            "RRS443_UNC",
            "RRS492",
            "RRS492_UNC",
            "RRS560",
            "RRS560_UNC",
            "RRS665",
            "RRS665_UNC",
            "RRS704",
            "RRS704_UNC",
            "RRS740",
            "RRS740_UNC",
            "RRS783",
            "RRS783_UNC",
            "RRS865",
            "RRS865_UNC",
            "SPM",
            "SPM_QI",
            "TUR",
            "TUR_QI",
            "crs",
            "lat",
            "lon",
            "time",
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
        if layer == "cmems_obs_oc_med_bgc_geophy_nrt_l3-hr_P1D-m_202105":
            if start is None:
                start = "2020-01-01T00:00:00Z"

            if end is None:
                end = "2023-10-24T23:59:59Z"

        if layer == "cmems_obs_oc_med_bgc_optics_nrt_l3-hr_P1D-m_202105":
            if start is None:
                start = "2020-01-01T00:00:00Z"

            if end is None:
                end = "2023-10-24T23:59:59Z"

        if layer == "cmems_obs_oc_med_bgc_transp_nrt_l3-hr_P1D-m_202105":
            if start is None:
                start = "2020-01-01T00:00:00Z"

            if end is None:
                end = "2023-10-24T23:59:59Z"

        if layer == "cmems_obs_oc_med_bgc_tur-spm-chl_nrt_l3-hr-mosaic_P1D-m_202107":
            if start is None:
                start = "2020-01-01T00:00:00Z"

            if end is None:
                end = "2023-10-24T23:59:59Z"

        super().__init__(
            layer=layer,
            area=area,
            variables=variables,
            start=start,
            end=end,
        )
