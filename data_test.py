data = {
        "word": "asd",
        "position": "ot",
        "syllable": "dff-sdf-sf",
        "cyrillic": "dfs",
        "noun": {
            'Bosh kelishik': 'abad', 
            'Qaratqich kelishigi': 'abadning', 
            'Tushum kelishigi': 'abadni', 
            'Jo‘nalish kelishigi': 'abadga', 
            'O‘rin-payt kelishigi': 'abadda', 
            'Chiqish kelishigi': 'abaddan'
        },
        "verb": [
            {
                'O‘tgan zamon': ['abadiylashdim', 'abadiylashding', 'abadiylashdi', 'abadiylashdik', 'abadiylashdingiz', 'abadiylashdilar', 'abadiylashmadim', 'abadiylashmading', 'abadiylashmadi', 'abadiylashmadik', 'abadiylashmadingiz', 'abadiylashmadilar']
            }, 
            {'Hozirgi zamon': ['abadiylashyapman', 'abadiylashyapsan', 'abadiylashyapti', 'abadiylashyapmiz', 'abadiylashyapsiz', 'abadiylashyaptilar', 'abadiylashmayapman', 'abadiylashmayapsan', 'abadiylashmayapti', 'abadiylashmayapmiz', 'abadiylashmayapsiz', 'abadiylashmayaptilar']}, {'Kelasi zamon': ['abadiylashmoqchiman', 'abadiylashmoqchisan','abadiylashmoqchi', 'abadiylashmoqchimiz', 'abadiylashmoqchisiz', 'abadiylashmoqchilar', 'abadiylashmoqchimasman', 'abadiylashmoqchimassan', 'abadiylashmoqchimas', 'abadiylashmoqchimasmiz', 'abadiylashmoqchimassiz', 'abadiylashmoqchimaslar']}]}


print(data['noun']['Bosh kelishik'])

print(data['verb'][0]['O‘tgan zamon'])