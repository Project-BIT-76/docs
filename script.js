// Конфигурация документации
const docs = [
    {
        path: 'README.md',
        title: 'Начало работы',
    },
    {
        path: 'README2.md',
        title: 'Работа с базой данных',
    },
    {
        path: 'README3.md',
        title: 'Демонстрация работы',
    }
    // Добавьте другие .md файлы здесь
];

// Функция для переключения темы
function toggleTheme() {
    const html = document.documentElement;
    const isDark = html.classList.contains('dark');
    
    // Переключаем класс темы
    html.classList.toggle('dark');
    
    // Переключаем стили highlight.js
    document.getElementById('light-theme-highlight').disabled = !isDark;
    document.getElementById('dark-theme-highlight').disabled = isDark;
    
    // Сохраняем предпочтение пользователя
    localStorage.setItem('theme', isDark ? 'light' : 'dark');
}

// Загрузка навигации
function loadNavigation() {
    const navigation = document.getElementById('navigation');
    docs.forEach(doc => {
        const link = document.createElement('a');
        link.href = '#' + doc.path;
        link.className = 'block p-2 hover:bg-gray-100 rounded transition-colors';
        link.textContent = doc.title;
        link.onclick = () => loadContent(doc.path);
        navigation.appendChild(link);
    });
}

// Загрузка контента
async function loadContent(path) {
    try {
        const response = await fetch(path);
        const text = await response.text();
        const content = document.getElementById('content');
        content.innerHTML = marked.parse(text);
        
        // Применяем подсветку синтаксиса ко всем блокам кода
        document.querySelectorAll('pre code').forEach((block) => {
            hljs.highlightElement(block);
        });
        
        // Обновление активной ссылки
        document.querySelectorAll('#navigation a').forEach(link => {
            link.classList.remove('active-link');
            if (link.getAttribute('href') === '#' + path) {
                link.classList.add('active-link');
            }
        });

        // Обновление URL
        window.location.hash = path;
    } catch (error) {
        console.error('Ошибка при загрузке документации:', error);
    }
}

// Инициализация
document.addEventListener('DOMContentLoaded', () => {
    loadNavigation();
    
    // Загрузка начальной страницы
    const initialPath = window.location.hash.slice(1) || docs[0].path;
    loadContent(initialPath);

    document.getElementById('theme-toggle').addEventListener('click', toggleTheme);

    // Установка начальной темы
    const savedTheme = localStorage.getItem('theme') || 
        (window.matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light');
    if (savedTheme === 'dark') {
        document.documentElement.classList.add('dark');
        document.getElementById('light-theme-highlight').disabled = true;
        document.getElementById('dark-theme-highlight').disabled = false;
    } else {
        document.getElementById('light-theme-highlight').disabled = false;
        document.getElementById('dark-theme-highlight').disabled = true;
    }

    // Настройка marked с highlight.js
    marked.setOptions({
        highlight: function(code, lang) {
            if (lang && hljs.getLanguage(lang)) {
                try {
                    return hljs.highlight(code, { language: lang }).value;
                } catch (err) {
                    console.error(err);
                }
            }
            return hljs.highlightAuto(code).value;
        }
    });

    document.getElementById('mobile-menu-button').addEventListener('click', function() {
        const navigation = document.getElementById('navigation');
        navigation.classList.toggle('hidden');
    });

    document.getElementById('navigation').addEventListener('click', function(e) {
        if (e.target.tagName === 'A' && window.innerWidth < 768) {
            this.classList.add('hidden');
        }
    });
});

// Обработка изменения хэша в URL
window.addEventListener('hashchange', () => {
    const path = window.location.hash.slice(1);
    if (path) {
        loadContent(path);
    }
});
  