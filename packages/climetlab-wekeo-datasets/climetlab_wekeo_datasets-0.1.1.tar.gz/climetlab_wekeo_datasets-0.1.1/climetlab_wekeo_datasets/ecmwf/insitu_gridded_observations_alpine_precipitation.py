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


class insitu_gridded_observations_alpine_precipitation(Main):
    name = "EO:ECMWF:DAT:INSITU_GRIDDED_OBSERVATIONS_ALPINE_PRECIPITATION"
    dataset = "EO:ECMWF:DAT:INSITU_GRIDDED_OBSERVATIONS_ALPINE_PRECIPITATION"

    choices = [
        "variable",
        "format_",
    ]

    string_selects = [
        "dataset_issue",
        "version",
    ]

    @normalize(
        "dataset_issue",
        [
            "LAPrec1871",
            "LAPrec1901",
        ],
        multiple=True,
    )
    @normalize(
        "version",
        [
            "1.1",
            "1.2",
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
    @normalize(
        "variable",
        [
            "precipitation",
        ],
    )
    def __init__(
        self,
        dataset_issue,
        version,
        format_=None,
        variable="precipitation",
    ):
        super().__init__(
            dataset_issue=dataset_issue,
            version=version,
            format_=format_,
            variable=variable,
        )
