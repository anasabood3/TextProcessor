import re
import pickle
from Item import Item
from data import load_data,save_data
from Cleaner import Cleaner

patterns = load_data("patterns.pkl")
cities = load_data("cities.pkl")


class SmartDetection():

    def __init__(self):
        self.cleaner = Cleaner()

    def extract_component(self, input, pattern):
        matched_components = re.search(pattern, input)
        output = re.sub(pattern, "", input,1)
        if matched_components:
            return self.cleaner.remove_appendages(matched_components.group(0)), output
        else:
            return None, output

    def smart_detect(self, input ,patterns):

        output = input
        for word in cities:
            if word in output and word !="":
                destination = word
                output =input.replace(word,"")
                print(destination)
                break
            else:
                destination = ""
        phone_number, output = self.extract_component(output, patterns["phone_number"])
        amount, output = self.extract_component(output, patterns["amount"])
        sender, output = self.extract_component(output, patterns["sender"])
        reciever, output = self.extract_component(output, patterns["receiver"])

        if (sender != None) and (reciever == None):
            reciever, output = self.extract_component(output, patterns["general_name"])
        elif (sender == None) and (reciever != None):
            sender, output = self.extract_component(output, patterns["general_name"])
        elif (sender == None) and (reciever == None):
            reciever, output = self.extract_component(output, patterns["general_name"])
            sender, output = self.extract_component(output, patterns["general_name"])
        new_item = Item( sender,reciever,phone_number, destination,amount)
        return new_item