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


class sis_european_risk_extreme_precipitation_indicators(Main):
    name = "EO:ECMWF:DAT:SIS_EUROPEAN_RISK_EXTREME_PRECIPITATION_INDICATORS"
    dataset = "EO:ECMWF:DAT:SIS_EUROPEAN_RISK_EXTREME_PRECIPITATION_INDICATORS"

    choices = [
        "format_",
    ]

    string_selects = [
        "city",
        "percentile",
        "period",
        "product_type",
        "return_period",
        "spatial_coverage",
        "temporal_aggregation",
        "variable",
    ]

    @normalize(
        "city",
        [
            "amadora",
            "amersfoort",
            "antwerp",
            "athens",
            "bilbao",
            "birmingham",
            "brussels",
            "bucharest",
            "budapest",
            "frankfurt_am_main",
            "koln",
            "london",
            "milan",
            "pamplona",
            "paris",
            "prague",
            "riga",
            "rimini",
            "stockholm",
            "vienna",
        ],
        multiple=True,
    )
    @normalize(
        "percentile",
        [
            "90th",
            "95th",
            "99th",
        ],
        multiple=True,
    )
    @normalize(
        "period",
        [
            "1950",
            "1951",
            "1952",
            "1953",
            "1954",
            "1955",
            "1956",
            "1957",
            "1958",
            "1959",
            "1960",
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
            "1989-2018",
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
        ],
        multiple=True,
    )
    @normalize(
        "product_type",
        [
            "e_obs",
            "eca_d",
            "era5",
            "era5_2km",
        ],
        multiple=True,
    )
    @normalize(
        "return_period",
        [
            "10-yrs",
            "100-yrs",
            "25-yrs",
            "5-yrs",
            "50-yrs",
        ],
        multiple=True,
    )
    @normalize(
        "spatial_coverage",
        [
            "city",
            "europe",
        ],
        multiple=True,
    )
    @normalize(
        "temporal_aggregation",
        [
            "30_year",
            "daily",
            "monthly",
            "yearly",
        ],
        multiple=True,
    )
    @normalize(
        "variable",
        [
            "maximum_1_day_precipitation",
            "maximum_5_day_precipitation",
            "number_of_consecutive_wet_days",
            "number_of_precipitation_days_exceeding_20mm",
            "number_of_precipitation_days_exceeding_fixed_percentiles",
            "number_of_wet_days",
            "precipitation_at_fixed_percentiles",
            "precipitation_at_fixed_return_periods",
            "standardised_precipitation_exceeding_fixed_percentiles",
            "total_precipitation",
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
        city,
        percentile,
        period,
        product_type,
        return_period,
        spatial_coverage,
        temporal_aggregation,
        variable,
        format_=None,
    ):
        super().__init__(
            city=city,
            percentile=percentile,
            period=period,
            product_type=product_type,
            return_period=return_period,
            spatial_coverage=spatial_coverage,
            temporal_aggregation=temporal_aggregation,
            variable=variable,
            format_=format_,
        )
