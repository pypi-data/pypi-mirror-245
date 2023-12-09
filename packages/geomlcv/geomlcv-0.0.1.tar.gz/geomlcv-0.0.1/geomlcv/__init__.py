import logging
import os

import ee


class GeoML:
    def __init__(self, model, data, label):
        self.model = model
        self.data = data
        self.label = label

    def _authenticate_gee(self):
        logging.info("Authenticating to Google Earth Engine...")
        credentials = ee.ServiceAccountCredentials(
            os.environ["GEE_SERVICE_ACCOUNT"],
            key_data=os.environ["GEE_SERVICE_ACCOUNT_JSON"],
        )
        ee.Initialize(credentials)
        logging.info("Authenticated to Google Earth Engine.")

    def test(self):
        print("GeoML test method")
        print("Model: ", self.model)
        print("Data: ", self.data)
        print("Label: ", self.label)
