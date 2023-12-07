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


class satellite_humidity_profiles(Main):
    name = "EO:ECMWF:DAT:SATELLITE_HUMIDITY_PROFILES"
    dataset = "EO:ECMWF:DAT:SATELLITE_HUMIDITY_PROFILES"

    choices = [
        "product_type",
        "variable",
        "format_",
    ]

    string_selects = [
        "month",
        "year",
    ]

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
        "year",
        [
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
        multiple=True,
    )
    @normalize(
        "product_type",
        [
            "radio_occultation_data",
            "reanalysis_data",
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
        month,
        year,
        product_type=None,
        format_=None,
        variable="all",
    ):
        super().__init__(
            month=month,
            year=year,
            product_type=product_type,
            format_=format_,
            variable=variable,
        )
