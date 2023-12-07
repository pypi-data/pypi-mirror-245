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


class reanalysis_cerra_pressure_levels(Main):
    name = "EO:ECMWF:DAT:REANALYSIS_CERRA_PRESSURE_LEVELS"
    dataset = "EO:ECMWF:DAT:REANALYSIS_CERRA_PRESSURE_LEVELS"

    choices = [
        "format_",
    ]

    string_selects = [
        "data_type",
        "day",
        "leadtime_hour",
        "month",
        "pressure_level",
        "product_type",
        "time",
        "variable",
        "year",
    ]

    @normalize(
        "data_type",
        [
            "ensemble_members",
            "reanalysis",
        ],
        multiple=True,
    )
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
        "leadtime_hour",
        [
            "1",
            "12",
            "15",
            "18",
            "2",
            "21",
            "24",
            "27",
            "3",
            "30",
            "4",
            "5",
            "6",
            "9",
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
        "pressure_level",
        [
            "1",
            "10",
            "100",
            "1000",
            "150",
            "2",
            "20",
            "200",
            "250",
            "3",
            "30",
            "300",
            "400",
            "5",
            "50",
            "500",
            "600",
            "7",
            "70",
            "700",
            "750",
            "800",
            "825",
            "850",
            "875",
            "900",
            "925",
            "950",
            "975",
        ],
        multiple=True,
    )
    @normalize(
        "product_type",
        [
            "analysis",
            "forecast",
        ],
        multiple=True,
    )
    @normalize(
        "time",
        [
            "00:00",
            "03:00",
            "06:00",
            "09:00",
            "12:00",
            "15:00",
            "18:00",
            "21:00",
        ],
        multiple=True,
    )
    @normalize(
        "variable",
        [
            "cloud_cover",
            "geopotential",
            "relative_humidity",
            "specific_cloud_ice_water_content",
            "specific_cloud_liquid_water_content",
            "specific_rain_water_content",
            "specific_snow_water_content",
            "temperature",
            "turbulent_kinetic_energy",
            "u_component_of_wind",
            "v_component_of_wind",
        ],
        multiple=True,
    )
    @normalize(
        "year",
        [
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
        ],
        multiple=True,
    )
    @normalize(
        "format_",
        [
            "grib",
            "netcdf",
        ],
    )
    def __init__(
        self,
        data_type,
        day,
        leadtime_hour,
        month,
        pressure_level,
        product_type,
        time,
        variable,
        year,
        format_=None,
    ):
        super().__init__(
            data_type=data_type,
            day=day,
            leadtime_hour=leadtime_hour,
            month=month,
            pressure_level=pressure_level,
            product_type=product_type,
            time=time,
            variable=variable,
            year=year,
            format_=format_,
        )
