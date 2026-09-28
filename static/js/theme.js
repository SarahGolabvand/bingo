try { document.documentElement.classList.toggle('dark', JSON.parse(localStorage.getItem('_x_darkMode') ?? 'true')); } catch (_) { document.documentElement.classList.add('dark'); }
