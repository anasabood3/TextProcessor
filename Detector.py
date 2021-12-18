from SmartDetection import SmartDetection
from Cleaner import Cleaner
from data import load_data

patterns = load_data("patterns.pkl")

import re


class Detector:
    def __init__(self):
        self.cleaner = Cleaner()
        self.smart_detector = SmartDetection()

    def split_messages(self, input):
        # for now
        whatsapp = r"(\n| *)?\[.*\].*: "
        new_input = re.sub(whatsapp, "#", input)
        items = new_input.split("#")
        return list(filter(lambda item: item != "", items))

    def detect(self, input, batch=False):
        extracted_items = []
        if batch:
            list_of_items = self.split_messages(input)

            if list_of_items:
                list_of_cleaned_items = []

                for item in list_of_items:
                    cleaned_item = self.cleaner.remove_strangers(self.cleaner.clean_extra_sapce(item))
                    list_of_cleaned_items.append(cleaned_item)
                for item in list_of_cleaned_items:
                    new_item = self.smart_detector.smart_detect(item, patterns)
                    extracted_items.append(new_item)
            else:
                return None
        else:
            cleaned_item = self.cleaner.remove_strangers(self.cleaner.clean_extra_sapce(input))
            new_item = self.smart_detector.smart_detect(cleaned_item, patterns)
            extracted_items.append(new_item)

        return extracted_items
