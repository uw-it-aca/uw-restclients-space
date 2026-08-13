# Copyright 2026 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0


import json
from restclients_core import models
from uw_space.utils import date_to_str, str_to_datetime


class Facility(models.Model):
    code = models.CharField(max_length=16)
    last_updated = models.DateTimeField(null=True)
    latitude = models.DecimalField(
        max_digits=12, decimal_places=10, null=True)
    longitude = models.DecimalField(
        max_length=13, decimal_places=10, null=True)
    name = models.CharField(max_length=96)
    number = models.CharField(max_length=16)
    type = models.CharField(max_length=32)
    site = models.CharField(max_length=96)
    status = models.CharField(max_length=64)
    center_point_url = models.CharField(max_length=96, null=True)
    city = models.CharField(max_length=64)
    state = models.CharField(max_length=8)
    street = models.CharField(max_length=64)
    post_code = models.CharField(max_length=16)
    map_url =  models.CharField(max_length=96, null=True)

    def __init__(self, *args, **kwargs):
        super(Facility, self).__init__(*args, **kwargs)

    @staticmethod
    def from_json(json_data):
        obj = Facility()
        obj.code = json_data.get("FacilityCode")
        obj.number = json_data.get("FacilityNumber")
        obj.last_updated = str_to_datetime(json_data.get("ModifiedDate"))
        obj.name = json_data.get("LongName")

        addresses = json_data.get("Addresses")
        if addresses and len(addresses) > 0:
            address = addresses[0]
            obj.street = address.get("StreetAddress")
            obj.city = address.get("City")
            obj.state = address.get("State")
            obj.post_code = address.get("PostalCode")

        cpoint = json_data.get("CenterPoint")
        if cpoint:
            cpoint_lat = cpoint.get("Latitude")
            cpoint_long = cpoint.get("Longitude")
            cpoint_href = cpoint.get("Href")
            if cpoint_lat and cpoint_long:
                obj.latitude = cpoint_lat
                obj.longitude = cpoint_long
                if cpoint_href and cpoint_href.startswith("http"):
                    obj.center_point_url = cpoint_href

        site_json = json_data.get("Site")
        if site_json:
            obj.site = site_json.get("Description")

        ftype = json_data.get("FacilityType")
        if ftype:
            obj.type = ftype.get("Description")

        maplink = json_data.get("MapLink")
        if maplink:
            obj.map_url = maplink.get("Href")

        obj.status = json_data.get("Status")
        return obj

    def json_data(self):
        return {
            "code": self.code,
            "last_updated": date_to_str(self.last_updated),
            "latitude": self.latitude,
            "longitude": self.longitude,
            "center_point_url": self.center_point_url,
            "name": self.name,
            "number": self.number,
            "site": self.site,
            "status": self.status,
            "type": self.type,
            "street": self.street,
            "city": self.city,
            "state": self.state,
            "post_code": self.post_code,
            "map_url": self.map_url,
        }

    def __str__(self):
        return json.dumps(self.json_data(), default=str)
