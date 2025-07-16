# 🚀 ІНСТРУКЦІЯ РОЗГОРТАННЯ НА VERCEL

## Метод 1: Швидке розгортання (рекомендується)

### 1. Підготовка репозиторію GitHub
```bash
# Якщо ще не створено GitHub репозиторій
git init
git add .
git commit -m "Initial commit"
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/safe.git
git push -u origin main
```

### 2. Розгортання через Vercel Dashboard
1. Перейдіть на [vercel.com](https://vercel.com)
2. Увійдіть через GitHub
3. Натисніть **"New Project"**
4. Виберіть ваш репозиторій `safe`
5. **ВАЖЛИВО**: У налаштуваннях проєкту встановіть:
   - **Root Directory**: `web-app`
   - **Framework Preset**: Other
6. Натисніть **"Deploy"**

### 3. Готово! 🎉
Ваш сайт буде доступний за адресою як `https://your-project.vercel.app`

---

## Метод 2: Через Vercel CLI

### 1. Встановіть Vercel CLI
```bash
npm install -g vercel
```

### 2. Розгорніть проєкт
```bash
cd web-app
vercel login
vercel

# Відповіді на питання:
# ? Set up and deploy "web-app"? [Y/n] Y
# ? Which scope do you want to deploy to? Your Name
# ? Link to existing project? [y/N] N
# ? What's your project's name? safe-calculator
# ? In which directory is your code located? ./
```

### 3. Налаштування домену (опціонально)
```bash
vercel --prod
vercel domains add your-domain.com
```

---

## Метод 3: Автоматичне розгортання

### 1. Клонування готового шаблону
```bash
git clone https://github.com/Quick-coder123/safe.git
cd safe/web-app
```

### 2. Прямий деплой
[![Deploy with Vercel](https://vercel.com/button)](https://vercel.com/new/clone?repository-url=https://github.com/Quick-coder123/safe&project-name=safe-calculator&root-directory=web-app)

---

## ⚙️ Налаштування після розгортання

### Перевірка роботи:
1. Відкрийте розгорнутий сайт
2. Перевірте вкладку "Калькулятор"
3. Зробіть тестовий розрахунок
4. Додайте тестового клієнта
5. Згенеруйте звіт

### Якщо щось не працює:
1. Перевірте логи в Vercel Dashboard
2. Переконайтесь що `Root Directory` встановлено на `web-app`
3. Перевірте що всі файли завантажились

---

## 🔧 Кастомізація

### Зміна тарифів:
Відредагуйте файл `api/index.py`, секцію `RATES`:
```python
RATES = {
    "dailyRates": [...],
    "insuranceRates": [...],
    "attorneyTariff": 300  # Ваш тариф
}
```

### Зміна дизайну:
Відредагуйте секцію `<style>` у файлі `public/index.html`

### Додавання функціональності:
1. Backend: додайте роути в `api/index.py`
2. Frontend: додайте JavaScript в `public/index.html`

---

## 📱 Тестування на різних пристроях

Після розгортання протестуйте на:
- 📱 **Мобільному телефоні**
- 💻 **Планшеті**  
- 🖥️ **Комп'ютері**
- 🌐 **Різних браузерах**

---

## 🆘 Вирішення проблем

### Помилка 404:
- Перевірте що `Root Directory` = `web-app`
- Переконайтесь що файл `public/index.html` існує

### Помилка API:
- Перевірте логи в Vercel Dashboard
- Переконайтесь що `requirements.txt` містить flask та flask-cors

### Проблеми з дизайном:
- Перевірте що CSS завантажується
- Відкрийте Developer Tools в браузері

---

## 🎯 Результат

Після успішного розгортання ви отримаєте:

✅ **Робочий веб-сайт** доступний 24/7  
✅ **Швидкий доступ** з будь-якого пристрою  
✅ **Автоматичні оновлення** при змінах у GitHub  
✅ **HTTPS** захищений зв'язок  
✅ **Глобальна доступність** через CDN  

**URL приклад**: `https://safe-calculator-your-name.vercel.app`

---

## 📞 Підтримка

Якщо виникли проблеми:
1. Перевірте [документацію Vercel](https://vercel.com/docs)
2. Подивіться логи у Vercel Dashboard
3. Створіть issue у GitHub репозиторії

**Готово! Ваш калькулятор сейфу тепер доступний онлайн! 🎉**
