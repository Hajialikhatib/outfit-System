# 🧵 JINSI YA KUANZA NGUO SYSTEM

## ✅ SERVERS ZIMEANZA!

### Django Backend: ✓ INAFANYA KAZI
- **URL**: http://localhost:8000
- **Admin**: http://localhost:8000/admin
- **API**: http://localhost:8000/api

---

## 📋 HATUA ZA KUANZISHA SYSTEM

### NJIA 1: Kutumia Scripts (RAHISI)

#### Fungua Terminal Mbili:

**Terminal 1 - Backend:**
```bash
cd ~/nguoSystem
./start-backend.sh
```

**Terminal 2 - Frontend:**
```bash
cd ~/nguoSystem
./start-frontend.sh
```

---

### NJIA 2: Kwa Mikono (Manual)

#### Terminal 1 - Django Backend:
```bash
cd ~/nguoSystem
source .venv/bin/activate
python manage.py runserver
```

#### Terminal 2 - React Frontend:
```bash
cd ~/nguoSystem/frontend
npm run dev
```

---

## 🌐 BAADA YA KUANZA SERVERS

1. **Fungua Browser yako** (Chrome, Firefox, etc.)

2. **Enda kwenye**: 
   ```
   http://localhost:5173
   ```

3. **Ukiona hii, umefanikiwa!**
   - Ukurasa wa "Karibu kwenye Nguo System"
   - Navigation bar juu
   - Buttons za "Anza Sasa" na "Ingia"

---

## 🔧 KAMA KUNA TATIZO

### Tatizo 1: "Connection Refused" kwenye Port 5173

**Suluhisho:**
```bash
# Terminal 2
cd ~/nguoSystem/frontend
npm run dev
```

Subiri sekunde chache hadi uone:
```
VITE ready in XXXms
➜ Local: http://localhost:5173/
```

### Tatizo 2: "Connection Refused" kwenye Port 8000

**Suluhisho:**
```bash
# Terminal 1
cd ~/nguoSystem
source .venv/bin/activate
python manage.py runserver
```

### Tatizo 3: Backend inafanya kazi lakini Frontend haionekani

**Angalia:**
1. Fungua http://localhost:5173 kwenye browser
2. SIKO http://localhost:8000

Frontend ni http://localhost:5173 ✓

---

## 📱 UKURASA UTAKAOONEKANA

### 1. Home Page (/)
- Hero section na "Karibu kwenye Nguo System"
- Features: Mitindo, Vipimo, Mtindo Maalum
- Buttons: "Anza Sasa", "Ingia"

### 2. Login (/login)
- Form ya kuingia
- Email na Password
- Button ya "Ingia"

### 3. Register (/register)
- Form ya kusajili
- Jina, Email, Simu, Jinsia, etc.
- Checkbox kwa washonaji

### 4. Styles (/styles)
- Gallery ya mitindo
- Filters: Zote, Kiume, Kike
- Picha na bei

### 5. Orders (/orders) - After Login
- Orodha ya oda zako
- Status ya kila oda
- Tarehe na bei

---

## 🎯 MAELEKEZO YA MATUMIZI

### Kusajili Akaunti:
1. Click "Sajili" kwenye navigation
2. Jaza form yote
3. Kama wewe ni mshonaji, bonyeza checkbox
4. Click "Sajili"

### Kuingia:
1. Click "Ingia"
2. Weka email na password
3. Click "Ingia"

### Kuangalia Mitindo:
1. Click "Mitindo" kwenye menu
2. Chagua filter (Zote/Kiume/Kike)
3. Angalia picha na bei

### Kuangalia Oda:
1. Ingia kwanza
2. Click "Oda Zangu"
3. Ona orodha ya oda zako

---

## ⚠️ MUHIMU!

### Lazima Servers Zote Mbili Zikwe Running:

✅ **Backend** (Django) - Port 8000  
✅ **Frontend** (React) - Port 5173

### Jinsi ya Kuacha:

Kwenye kila terminal, bonyeza:
```
CTRL + C
```

---

## 🆘 TATIZO? CONTACT

Kama bado kuna tatizo:

1. **Check Ports:**
   ```bash
   lsof -i :8000  # Django
   lsof -i :5173  # React
   ```

2. **Check Logs:**
   - Angalia output kwenye terminals
   - Kama kuna error, soma message

3. **Restart Everything:**
   ```bash
   # Acha servers (CTRL+C kwenye terminals zote)
   
   # Anza upya
   ./start-backend.sh   # Terminal 1
   ./start-frontend.sh  # Terminal 2
   ```

---

## ✅ QUICK CHECK

Kabla ya kutumia, hakikisha:

- [ ] Virtual environment imeactivate
- [ ] Django inafanya kazi (http://localhost:8000)
- [ ] React inafanya kazi (http://localhost:5173)
- [ ] Browser umefungua http://localhost:5173
- [ ] Unaona ukurasa wa Home

---

**🎉 FURAHIA KUTUMIA NGUO SYSTEM!**
