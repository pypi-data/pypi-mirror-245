#!/usr/bin/env python3
# (C) Copyright 2023 European Centre for Medium-Range Weather Forecasts.
# This software is licensed under the terms of the Apache Licence Version 2.0
# which can be obtained at http://www.apache.org/licenses/LICENSE-2.0.
# In applying this licence, ECMWF does not waive the privileges and immunities
# granted to it by virtue of its status as an intergovernmental organisation
# nor does it submit to any jurisdiction.
from __future__ import annotations

from climetlab.decorators import normalize

from climetlab_wekeo_datasets.clms.main import Main


class cgls_global_ndvi_st(Main):
    name = "EO:CLMS:DAT:CGLS_GLOBAL_NDVI_ST"
    dataset = "EO:CLMS:DAT:CGLS_GLOBAL_NDVI_ST"

    @normalize("start", "date(%Y-%m-%dT%H:%M:%SZ)")
    @normalize("end", "date(%Y-%m-%dT%H:%M:%SZ)")
    def __init__(
        self,
        start="1999-01-01T00:00:00Z",
        end="2015-12-21T00:00:00Z",
    ):
        super().__init__(
            start=start,
            end=end,
        )
