# Frontend ya Nguo System

Frontend ya kisasa iliyotengenezwa kwa React na Vite kwa mfumo wa Nguo System.

## Vipengele Vikuu

- ✅ **Authentication** - Login na Register kwa Swahili
- ✅ **Styles Management** - Angalia na chagua mitindo ya nguo
- ✅ **Orders Management** - Oda na fuatilia oda zako
- ✅ **Responsive Design** - Inafanya kazi vizuri kwenye simu na kompyuta
- ✅ **Protected Routes** - Ulinzi wa kurasa zinazohitaji kuingia
- ✅ **API Integration** - Imeunganishwa na Django backend

## Teknolojia Zilizotumika

- **React 19** - UI Library
- **React Router** - Navigation
- **Axios** - HTTP Client
- **Vite** - Build Tool
- **CSS3** - Styling

## Jinsi ya Kutumia

### 1. Sanikisha Dependencies

```bash
npm install
```

### 2. Anzisha Development Server

```bash
npm run dev
```

Frontend itakuwa inapatikana kwenye: http://localhost:5173

### 3. Build kwa Production

```bash
npm run build
```

## Structure ya Project

```
src/
├── components/        # Reusable components
│   ├── Navbar.jsx
│   └── ProtectedRoute.jsx
├── pages/            # Page components
│   ├── Home.jsx
│   ├── Login.jsx
│   ├── Register.jsx
│   ├── Styles.jsx
│   └── Orders.jsx
├── context/          # React Context
│   └── AuthContext.jsx
├── services/         # API services
│   └── api.js
├── App.jsx          # Main App component
└── main.jsx         # Entry point
```

## API Configuration

Backend API inapatikana kwenye: `http://localhost:8000/api`

Endpoints:
- `/api/accounts/` - Authentication
- `/api/styles/` - Mitindo
- `/api/orders/` - Oda
- `/api/feedback/` - Maoni

## Features Zijazo

- [ ] Feedback submission
- [ ] Custom style requests
- [ ] Tailor dashboard
- [ ] Admin dashboard
- [ ] Image upload preview
- [ ] Order creation form
- [ ] Real-time notifications

## Maelezo Zaidi

Soma documentation kamili kwenye: `/docs`
