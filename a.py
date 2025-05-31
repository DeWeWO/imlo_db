def collect_data(word):
    data = {
        "word": "",
        "position": "",
        "syllable": "",
        "cyrillic": "",
        "noun": {},
        "verb": {}
    }
    
    link = f"https://imlo.uz/word/{word}"
    try:
        response = requests.get(link, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')

        # So'z
        specific_h1 = soup.find('h1', class_='font-bold')
        if specific_h1:
            data["word"] = specific_h1.text.strip()

        # Turkumi
        specific_div = soup.find('div', class_='italic')
        if specific_div:
            data["position"] = specific_div.text.strip()

        # Agar turkumda "Ot" so'zi bo'lsa, noun ma'lumotlarini qo'shish
        if specific_div and "ot" in specific_div.text.strip().lower():
            flex_lis = soup.find_all('li', class_='flex')
            for flex_li in flex_lis:
                neutral_span = flex_li.find('span', class_='text-neutral-400')
                capitalize_span = flex_li.find('span', class_='capitalize')
                if neutral_span and capitalize_span:
                    category_info = neutral_span.text.strip()
                    changed_word = capitalize_span.text.strip()
                    data["noun"][category_info] = changed_word

        # Agar turkumda "Fe'l" so'zi bo'lsa, verb ma'lumotlarini qo'shish
        if specific_div and "fe'l" in specific_div.text.strip().lower():
            h_tags = soup.find_all(['h3', 'h4'], class_='text-neutral-400')
            for h_tag in h_tags:
                category_info = h_tag.text.strip()
                data["verb"][category_info] = []
                next_sibling = h_tag.find_next_sibling('ul', class_='space-y-4')
                if next_sibling:
                    li_tags = next_sibling.find_all('li')
                    for li in li_tags:
                        changed_word = li.get_text(strip=True)
                        data["verb"][category_info].append(changed_word)

        # Bo'g'in
        parent_div = soup.find('div', class_='space-y-4')
        if parent_div:
            all_ps = parent_div.find_all('p')
            if len(all_ps) >= 2:
                second_p = all_ps[1]
                span_in_p = second_p.find('span')
                if span_in_p:
                    data["syllable"] = span_in_p.text.strip()
            
            # Kirillcha ko'rinishi
            if len(all_ps) >= 4:
                fourth_p = all_ps[3]
                span_in_p = fourth_p.find('span')
                if span_in_p:
                    data["cyrillic"] = span_in_p.text.strip()
        
        return data
    
    except Exception as e:
        print(f"datani to'ldirishda muammo ({word}): {e}")
        return data