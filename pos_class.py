import query

def noun(data):
    try:
        result=True
        if query.save_to_word(data["word"], data["position"], data["syllable"], data["cyrillic"]):
            word_id=query.get_word_id(data["word"])

            if not query.save_category(data["position"]):
                result = False

            for key in data["noun"].keys():
                
                if query.save_category(key):
                    key_id=query.get_category_id(key)
                    if not query.save_to_wordInfo(word_id,key_id,data["noun"][key]):
                        result=False# Agar yozishda xato bo'lsa, result=False
                    else:
                        pass
                else:
                    result = False# Agar kategoriya yozilmagan bo'lsa
        else:
            result = False# Agar so'z yozilmagan bo'lsa
        return result
    except:
        print("noun yozishda muammo")


def verb(data):
    try:
        result=True
        if query.save_to_word(data["word"], data["position"], data["syllable"], data["cyrillic"]):
            word_id=query.get_word_id(data["word"])

            if not query.save_category(data["position"]):
                result = False

            for key in data["verb"].keys():
                
                if query.save_category(key):
                    key_id=query.get_category_id(key)
                    if not query.save_to_wordInfo(word_id,key_id,data["verb"][key]):
                        result=False# Agar yozishda xato bo'lsa, result=False
                    else:
                        pass
                else:
                    result = False# Agar kategoriya yozilmagan bo'lsa
        else:
            result = False# Agar so'z yozilmagan bo'lsa
        return result
    except:
        print("verb yozishda muammo")

def other(data):
    try:
        result=True
        # Agar position da "Ot" so'zi bo'lsa, noun funksiyasiga yo'naltirish
        if "ot" in data["position"].lower():
            return noun(data)
        
        if query.save_to_word(data["word"], data["position"], data["syllable"], data["cyrillic"]):

            if not query.save_category(data["position"]):
                result = False

        else:
            result = False# Agar so'z yozilmagan bo'lsa
        return result
    except:
        print("other yozishda muammo")