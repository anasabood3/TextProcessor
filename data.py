import pickle
#
# patterns = {
#     "phone_number": r"(00|\+|0|9|\u0660|\u0660\u0660)[0-9, ,\u0660-\u0669]{8,}",
#
#     "sender": r"(ال|ل|ا|تال)?(مرسل)( *)(:|.| *|,|=)*([\u0621-\u064A ])+",
#
#     "amount": r"((مبلغ)?(ال|ا|ل|تا))?([0-9,\u0660-\u0669]{1,8}((\.|,)[0-9,\u0660-\u0669]{1,7})*)( )*(\$|(دولار)|(سوري)|(\u0644(\.|لير(ه|ة) )*\u0633))?",
#
#     "receiver": r"(تال|ال|ل|ا)?(مرسل ((ا|إ)ليه|له)|مستلم|مستفيد|(ا|إ)لى)( *)(:|.*| *|,|=)?(.)*",
#
#     "general_name": r"((([\u0621-\u064A]|[a-z,A-Z]){2,}) ){1,}((([\u0621-\u064A]|[a-z,A-Z]){2,}))",
#
#     "destination": r"(ال|ل|ا|تا)?((\u0648)?\u062C\u0647(\u0629|\u0647)|(مكان)|(مدين(ة|ه))|((إ|ا)لى))([\u0621-\u064A ])*",
#
#     # "whatsapp": r"^(\n| *)?\[.*\].*: "
#
# }
# #
# #
# Errors = {
#     "Saving Error": "Error in Saving File \n Check if it`s already opened",
#     "Batch Recommended": "Too Long text input, Batch Mode is Recommended",
#     "Empty List": "List is Empty"
# }


def load_data(fname):
    with open("assets/data/" + str(fname), 'rb') as data:
        object = pickle.load(data)
        return object


def save_data(fname, object):
    with open("assets/data/" + str(fname), 'wb') as data:
        pickle.dump(object, data)