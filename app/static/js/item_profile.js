// static/js/item_profile.js

function addToCart(url) {
    const csrfToken = document.getElementById('csrf_token').value;

    fetch(url, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrfToken
        }
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            console.log('Успешно добавлено в корзину:', data);
            var button = document.getElementById('addToCartButton');
            button.classList.remove('btn-primary');
            button.classList.add('btn-success');
            button.textContent = 'Добавлено в корзину';
        } else {
            console.error('Ошибка при добавлении в корзину:', data);
        }
    })
    .catch(error => {
        console.error('Ошибка при выполнении POST-запроса:', error);
    });
}