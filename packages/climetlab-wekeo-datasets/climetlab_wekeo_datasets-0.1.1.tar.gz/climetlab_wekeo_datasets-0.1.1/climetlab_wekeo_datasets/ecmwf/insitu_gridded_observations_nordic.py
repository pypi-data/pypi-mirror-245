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


class insitu_gridded_observations_nordic(Main):
    name = "EO:ECMWF:DAT:INSITU_GRIDDED_OBSERVATIONS_NORDIC"
    dataset = "EO:ECMWF:DAT:INSITU_GRIDDED_OBSERVATIONS_NORDIC"

    choices = [
        "format_",
    ]

    string_selects = [
        "day",
        "month",
        "product_type",
        "spatial_interpolation_method",
        "variable",
        "version",
        "year",
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
        "product_type",
        [
            "consolidated",
            "provisional",
        ],
        multiple=True,
    )
    @normalize(
        "spatial_interpolation_method",
        [
            "type_1",
            "type_2",
        ],
        multiple=True,
    )
    @normalize(
        "variable",
        [
            "maximum_temperature",
            "mean_temperature",
            "minimum_temperature",
            "precipitation",
        ],
        multiple=True,
    )
    @normalize(
        "version",
        [
            "22.03",
            "22_09",
            "23_03",
            "23_09",
        ],
        multiple=True,
    )
    @normalize(
        "year",
        [
            "1961",
            "1962",
            "1963",
            "1964",
            "1965",
            "1966",
            "1967",
            "1968",
            "1969",
            "1970",
            "1971",
            "1972",
            "1973",
            "1974",
            "1975",
            "1976",
            "1977",
            "1978",
            "1979",
            "1980",
            "1981",
            "1982",
            "1983",
            "1984",
            "1985",
            "1986",
            "1987",
            "1988",
            "1989",
            "1990",
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
        day,
        month,
        product_type,
        spatial_interpolation_method,
        variable,
        version,
        year,
        format_=None,
    ):
        super().__init__(
            day=day,
            month=month,
            product_type=product_type,
            spatial_interpolation_method=spatial_interpolation_method,
            variable=variable,
            version=version,
            year=year,
            format_=format_,
        )
