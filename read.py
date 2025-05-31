import requests
from bs4 import BeautifulSoup
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
import time
from urllib.parse import urljoin
from pos_class import noun, verb, other

def run(max_words):
    count_words = 0
    last_data=get_last_data()
    

    try:
        base_url = "https://imlo.uz"
        letter_links = collect_letter_links(base_url)
        
        if len(last_data)==4:
            l_index=letter_links.index(last_data[0])
            l_page=int(last_data[1])
            l_word=last_data[2]
            l_count=int(last_data[3])
        else:
            l_index=0
            l_page=1
            l_count=0
            l_word=''
            l_word_index=-1
        
        for letter_link in letter_links:
            
            if letter_links.index(letter_link)<l_index:
                continue
            print(letter_link)
            page_count = check_letter_pages(letter_link)
            
            for page in range(l_page, page_count + 1):
                print(page)
                page_url = f"{letter_link}?page={page}"
                words = collect_words_from_page(page_url)
                
                if len(l_word)>0:
                    
                    try:
                        l_word_index=words.index(l_word)
                    except:
                        l_word_index=-1
                    
                
                for word in words:
                    if words.index(word)<=l_word_index:
                        continue
                    
                    print(word)
                    data = collect_data(word, letter_link, page)
                    # Har bir so'z uchun data lug'atini chop etish
                    
                    print(count_words)
                    
                    # pos_class moduli o'rniga hozircha True deb faraz qilamiz
                    if data["position"].lower() == "ot":
                        if noun(data):
                            count_words += 1
                    elif data["position"].lower() == "fe'l":
                        if verb(data):
                            count_words += 1
                    else:
                        if other(data):
                            count_words += 1
                    
                    # Maksimal so'zlar soniga yetdikmi, tekshirish
                    if count_words >= max_words:
                        print(f"Umumiy yig'ilgan so'zlar soni: {count_words}")
                        write_last_data(str(letter_link), str(page), str(word), str(l_count+count_words))
                        return
                
                l_word=''
                l_word_index=-1
            l_page=1       
    except Exception as e:
        print(f"run funksiyasida muammo bo'ldi: {e}")

def collect_letter_links(base_url):
    try:
        session = requests.Session()
        session.headers.update({'User-Agent': 'Mozilla/5.0'})
        response = session.get(base_url, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        grid_div = soup.find('div', class_='grid')
        letter_links = grid_div.find_all('a', class_='py-4 w-full')
        return [urljoin(base_url, link['href']) for link in letter_links]
    except Exception as e:
        print(f"collect_links da xatolik: {e}")
        return []

def check_letter_pages(letter_url):
    try:
        response = requests.get(letter_url, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        pagination = soup.find('span', class_='relative z-0 inline-flex space-x-2 justify-center w-full')
        if not pagination:
            return 1
        page_links = pagination.find_all('a', href=True)
        last_page = 1
        for link in page_links:
            href = link.get('href')
            if 'page=' in href:
                page_num = int(href.split('page=')[-1])
                last_page = max(last_page, page_num)
        return last_page
    except Exception as e:
        print(f"check_letterda xato: {e}")
        return 1

def collect_words_from_page(page_url):
    try:
        response = requests.get(page_url, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        word_list = soup.find('ul', class_='columns-1 lg:columns-4 gap-12')
        if not word_list:
            return []
        words = []
        for li in word_list.find_all('li'):
            word_link = li.find('a', class_='py-2 pr-4')
            if word_link and word_link.text.strip():
                words.append(word_link.text.strip())
        return words
    except Exception as e:
        print(f"collect_words_from_page xato: {e}")
        return []

def collect_data(word, letter_link, page, max_retries=3):
    data = {
        "word": "",
        "position": "",
        "syllable": "",
        "cyrillic": "",
        "noun": {},
        "verb": {}
    }
    
    link = f"https://imlo.uz/word/{word}"
    for attempt in range(max_retries):
        try:
            response = requests.get(link, timeout=15)
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

            # Ma'lumotlarning to'ldirilganligini tekshirish
            if not data["word"] and not data["position"] and not data["syllable"] and not data["cyrillic"]:
                print(f"Xato: '{word}' uchun ma'lumotlar to'liq yig'ilmadi. Faylga yozildi")
                # Xato so'zni .txt faylga yozish
                with open("error_words.txt", "a", encoding="utf-8") as file:
                    file.write(f"{letter_link} {page} {word}\n")
                return None  # Bo'sh yoki to'liqsiz ma'lumotni qaytarmaymiz
            
            return data
        
        except (requests.exceptions.Timeout, requests.exceptions.ConnectionError) as e:
            print(f"Xato: '{word}' uchun urinish {attempt + 1}/{max_retries}: {e}")
            if attempt < max_retries - 1:
                time.sleep(2 ** attempt)  # Eksponensial backoff
                continue
            else:
                print(f"Xato: '{word}' so'zi uchun ma'lumot yig'ilmadi (timeout yoki ulanish xatosi). Faylga yozildi")
                with open("error_words.txt", "a", encoding="utf-8") as file:
                    file.write(f"{letter_link} {page} {word}\n")
                return None
        
        except Exception as e:
            print(f"Xato: '{word}' so'zi uchun ma'lumot yig'ishda muammo: {e}.  Faylga yozildi")
            # Xato so'zni .txt faylga yozish
            with open("error_words.txt", "a", encoding="utf-8") as file:
                file.write(f"{letter_link} {page} {word}\n")
            return None  # Xato yuz bersa None qaytariladi
        
        except requests.exceptions.ConnectionError:
            print(f"Internet ulanishida muammo: '{word}' uchun ma'lumot yig'ilmadi.  Faylga yozildi")
            # Xato so'zni .txt faylga yozish
            with open("error_words.txt", "a", encoding="utf-8") as file:
                file.write(f"{letter_link} {page} {word}\n")
            return None  # Xato yuz bersa None qaytariladi
        
        except:
            print("Qandaydir g'alati muammo tifayli dastur to'xtadi.")
            return None

def write_last_data(link, page, word, count):
    with open('last_data.txt', 'w', encoding='utf-8') as f:
        f.write(str(link)+' ')
        f.write(str(page)+' ')
        f.write(str(word)+' ')
        f.write(count)

def get_last_data():
    with open('last_data.txt', 'r', encoding='utf-8') as f:
        row=f.readline().split()
        return row
    return []

if __name__ == "__main__":
    run()
