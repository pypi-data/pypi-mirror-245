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


class insitu_observations_gnss(Main):
    name = "EO:ECMWF:DAT:INSITU_OBSERVATIONS_GNSS"
    dataset = "EO:ECMWF:DAT:INSITU_OBSERVATIONS_GNSS"

    choices = [
        "network_type",
        "year",
        "format_",
    ]

    string_selects = [
        "day",
        "month",
        "variable",
    ]

    @normalize("area", "bounding-box(list)")
    @normalize(
        "day",
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
            "13",
            "14",
            "15",
            "16",
            "17",
            "18",
            "19",
            "20",
            "21",
            "22",
            "23",
            "24",
            "25",
            "26",
            "27",
            "28",
            "29",
            "30",
            "31",
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
        "variable",
        [
            "total_column_water_vapour",
            "total_column_water_vapour_combined_uncertainty",
            "total_column_water_vapour_era5",
            "zenith_total_delay",
            "zenith_total_delay_random_uncertainty",
        ],
        multiple=True,
    )
    @normalize(
        "network_type",
        [
            "epn",
            "igs",
        ],
    )
    @normalize(
        "year",
        [
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
        ],
    )
    @normalize(
        "format_",
        [
            "csv-lev.zip",
            "csv-obs.zip",
        ],
    )
    def __init__(
        self,
        area=None,
        day=None,
        month=None,
        variable=None,
        network_type=None,
        year=None,
        format_=None,
    ):
        super().__init__(
            area=area,
            day=day,
            month=month,
            variable=variable,
            network_type=network_type,
            year=year,
            format_=format_,
        )
