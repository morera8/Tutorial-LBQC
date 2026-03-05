// Navigation functionality
document.addEventListener('DOMContentLoaded', function() {
    const navItems = document.querySelectorAll('.nav-item');
    
    // Highlight current page in sidebar
    const currentPage = window.location.pathname.split('/').pop() || 'index.html';
    
    navItems.forEach(item => {
        const itemPage = item.getAttribute('href');
        if (itemPage === currentPage) {
            item.classList.add('active');
        }
        
        item.addEventListener('click', function(e) {
            // Remove active class from all items
            navItems.forEach(nav => nav.classList.remove('active'));
            // Add active class to clicked item
            this.classList.add('active');
        });
    });

    // Keyboard navigation
    document.addEventListener('keydown', (e) => {
        const activeItem = document.querySelector('.nav-item.active');
        const allItems = Array.from(navItems);
        const currentIndex = allItems.indexOf(activeItem);

        if (e.key === 'ArrowDown' && currentIndex < allItems.length - 1) {
            allItems[currentIndex + 1].click();
            e.preventDefault();
        } else if (e.key === 'ArrowUp' && currentIndex > 0) {
            allItems[currentIndex - 1].click();
            e.preventDefault();
        }
    });
});
// Manter posição da sidebar ao navegar entre páginas
window.addEventListener('load', function() {
    // Salvar posição do scroll da sidebar antes de sair da página
    window.addEventListener('beforeunload', function() {
        const sidebar = document.querySelector('.sidebar');
        if (sidebar) {
            sessionStorage.setItem('sidebarScroll', sidebar.scrollTop);
        }
    });

    // Restaurar posição do scroll da sidebar ao carregar a página
    const savedScroll = sessionStorage.getItem('sidebarScroll');
    if (savedScroll) {
        const sidebar = document.querySelector('.sidebar');
        if (sidebar) {
            sidebar.scrollTop = parseInt(savedScroll);
        }
    }
});