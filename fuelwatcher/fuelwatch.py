"""
    fuelwatcher - A python module for scraping XML data from the Western
    Australian governments Fuel Watch initiative.

    <https://www.fuelwatch.wa.gov.au>

        Copyright (C) 2018, Daniel Michaels
        Copyright (C) 2020, Alyssa Smith
"""
from .constants import PRODUCT, REGION, BRAND, SUBURB

from xml.etree import ElementTree
import requests

URL = 'http://fuelwatch.wa.gov.au/fuelwatch/fuelWatchRSS'

class FuelWatch:
    """Client for FuelWatch RSS Feed. """

    def query(self, product: int = None, suburb: str = None,
              region: int = None, brand: int = None, surrounding: str = None,
              day: str = None):
        """
        Returns FuelWatch data based on query parameters

        If all parameters are None it will return all stations with
        product set to Unleaded Petrol.

        :param product: Takes in a integer from the following table.
        1 - Unleaded Petrol     2 - Premium Unleaded
        4 - Diesel              5 - LPG
        6 - 98 RON              10 - E85
        11 - Brand diesel

        :param suburb: Takes a valid Western Australian suburb.

        Full list found in utils.suburbs

        :param region: FuelWatch seperates WA into regions that take an

        integer. Refer to utils.region for a listing.

        :param brand: Takes in any valid registered WA fuel station. Refer to
        utils.brand for the full list.

        :param surrounding: boolean 'yes/no' that will return surrounding
        suburbs when used in conjuction with the suburb parameter. Must be set
        to 'no' explicitly, otherwise returns True.

        :param day: Capable of four argument types:
            - today (this is the default)
            - tomorrow (only available after 2:30PM)
            - yesterday
            - DD/MM/YYYY (only prices for the last week, e.g. 23/08/2016)

            returns today if not set.

        :param to_dicts: Determines if this returns a list of dicts

        :return: self.to_dicts(response.content)
        """

        payload = dict()
        payload['Product'] = product
        payload['Suburb'] = suburb
        payload['Region'] = region
        payload['Brand'] = brand
        payload['Surrounding'] = surrounding
        payload['Day'] = day

        response = requests.get(URL, timeout=30, params=payload)
        if response.status_code == 200:
            return self.to_dicts(response.content)

    def to_dicts(self, feed):
        """
        Given page content parses through the RSS XML and returns only 'item'
        data which contains fuel station information.

        :param result: url response.content from FuelWatch.query()

        :return: a list of dictionaries from the XML content.
        """

        dom = ElementTree.fromstring(feed)
        items = dom.findall('channel/item')

        out = []
        for elem in items:
            dic = dict()

            dic['title'] = elem.find('title').text
            dic['description'] = elem.find('description').text
            dic['brand'] = elem.find('brand').text
            dic['date'] = elem.find('date').text
            dic['price'] = elem.find('price').text
            dic['trading-name'] = elem.find('trading-name').text
            dic['location'] = elem.find('location').text
            dic['address'] = elem.find('address').text
            dic['phone'] = elem.find('phone').text
            dic['latitude'] = elem.find('latitude').text
            dic['longitude'] = elem.find('longitude').text
            dic['site-features'] = elem.find('site-features').text
            out.append(dic)

        return out

    class Product:
        ULP = 1
        PULP = 2
        DIESEL = 4
        LPG = 5
        NINETYEIGHT = 6
        E85 = 10
        BDIESEL = 11
