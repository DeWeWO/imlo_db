# 🧠 imlo.uz Word Parser

**imlo.uz Word Parser** — bu Python dasturi bo‘lib, u [imlo.uz](https://imlo.uz) vebsaytidan o‘zbek tilidagi so‘zlarni to‘liq morfologik ma'lumotlari bilan yig‘ib, ularni MySQL bazasiga yozish uchun foydalaniladi. U avtomatik tarzda harflar, sahifalar, va so‘zlar bo‘ylab yuradi, kerakli grammatik ma'lumotlarni ajratadi va so‘z turkumiga qarab mos funksiyaga yuboradi.

---

## ⚙️ Imkoniyatlari

- 🔤 Har bir harfga tegishli so‘zlar ro‘yxatini avtomatik yig‘adi
- 📄 Har bir so‘z sahifasidan:
  - So‘zning o‘zi
  - So‘z turkumi (ot, fe’l, boshqa)
  - Bo‘g‘inli yozilishi
  - Kirill yozuvi
  - Fe’l va otlarga xos morfologik shakllarni
- 🔁 Avtomatik davom ettirish (`last_data.txt` orqali)
- ⛔ Xatoliklar uchun `error_words.txt` log fayl
- 📦 Har bir so‘z tegishli `pos_class` modulidagi (`noun`, `verb`, `other`) funksiyaga yuboriladi (bu funksiyalar orqali ma'lumotlar bazaga yozilishi kutiladi)

---

## 🗃 Tizim Talablari

- Python 3.7+
- MySQL (backendda ishlatiladi, `query.py` orqali)

### Python kutubxonalar:
- `requests`
- `beautifulsoup4`
- `urllib3`

```bash
pip install -r requirements.txt
