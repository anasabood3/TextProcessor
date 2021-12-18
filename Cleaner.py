

import re


class Cleaner():
    def clean_extra_sapce(self,input):
        return re.sub(r" +", " ", input)
    def clean_extra_newlines(self,input):
        return re.sub(r"\n+", "\n", input)
    def clean_extra_dots(self,input):
        return re.sub(r"\.+", ".", input)
    def clean_extra_commas(self,input):
        return re.sub(r"\,+", ",", input)
    def clean_extra_colons(self,input):
        return re.sub(r"\:+", ":", input)
    def clean_extra_dollar(self,input):
        return re.sub(r"\$+", "$", input)

    def remove_strangers(self,input):
        output = ""
        for i in input:
            if i.isdigit() or i.isalpha() or i in [".",",",":"," ","$","\n"]:
                output += i
        return output

    def remove_appendages(self,text_to_clean):
        patters_list = [r"(مرسل|واتس|عادي|مستلم)( )*\.",r"(ال)?(مستلم|مرسل|وجهة|مكان|مبلغ|هاتف|مستفيد|منطقة|شركة)( )*(\/|:|\.)?", r""]
        cleaned_text = re.sub(patters_list[0], "", text_to_clean)
        cleaned_text = re.sub(patters_list[1], "", cleaned_text)
        return cleaned_text

