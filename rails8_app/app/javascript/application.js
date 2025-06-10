// Configure your import map in config/importmap.rb. Read more: https://github.com/rails/importmap-rails
import "htmx.org"
document.addEventListener('DOMContentLoaded', () => {
    const token = document.querySelector('meta[name="csrf-token"]').getAttribute('content');
    document.body.addEventListener('htmx:configRequest', (event) => {
        event.detail.headers['X-CSRF-Token'] = token;
    });
});
// Import and register any other JavaScript files you need