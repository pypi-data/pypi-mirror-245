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


class satellite_fire_radiative_power(Main):
    name = "EO:ECMWF:DAT:SATELLITE_FIRE_RADIATIVE_POWER"
    dataset = "EO:ECMWF:DAT:SATELLITE_FIRE_RADIATIVE_POWER"

    choices = [
        "product_type",
        "time_aggregation",
        "horizontal_aggregation",
        "year",
        "variable",
        "format_",
    ]

    string_selects = [
        "day",
        "month",
        "version",
    ]

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
        "version",
        [
            "1.0",
        ],
        multiple=True,
    )
    @normalize(
        "product_type",
        [
            "gridded",
            "table_summary",
        ],
    )
    @normalize(
        "time_aggregation",
        [
            "27_days",
            "day",
            "month",
        ],
    )
    @normalize(
        "horizontal_aggregation",
        [
            "0_1_degree_x_0_1_degree",
            "0_25_degree_x_0_25_degree",
        ],
    )
    @normalize(
        "year",
        [
            "2020",
            "2021",
        ],
    )
    @normalize(
        "format_",
        [
            "tgz",
            "zip",
        ],
    )
    @normalize(
        "variable",
        [
            "all",
        ],
    )
    def __init__(
        self,
        day,
        month,
        version,
        product_type=None,
        time_aggregation=None,
        horizontal_aggregation=None,
        year=None,
        format_=None,
        variable="all",
    ):
        super().__init__(
            day=day,
            month=month,
            version=version,
            product_type=product_type,
            time_aggregation=time_aggregation,
            horizontal_aggregation=horizontal_aggregation,
            year=year,
            format_=format_,
            variable=variable,
        )
