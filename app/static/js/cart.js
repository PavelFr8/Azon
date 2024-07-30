// static/js/cart.js

function getCsrfToken() {
    return document.querySelector('meta[name="csrf-token"]').getAttribute('content');
}

function updateTotalPrice(price) {
    const totalPriceElement = document.getElementById('total-price');
    let currentTotal = parseFloat(totalPriceElement.innerText.replace('Итого: ', '').replace(' ₽', ''));
    currentTotal -= price;
    totalPriceElement.innerText = `Итого: ${currentTotal.toString().replace(/(\.\d*[1-9])0+$|\.0*$/, '$1')} ₽`;
}

function deleteFromCart(url, article, price) {
    console.log('Attempting to delete item with article:', article);
    console.log('CSRF Token:', getCsrfToken());
    console.log('Request URL:', url);

    fetch(url, {
        method: 'DELETE',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCsrfToken()
        }
    })
    .then(response => {
        console.log('Response status:', response.status);
        if (response.status === 204) {
            return { success: true };
        }
        return response.json();
    })
    .then(data => {
        console.log('Response data:', data);
        if (data.success) {
            console.log('Товар успешно удален из корзины:', data);
            const itemElement = document.getElementById(`item-${article}`);
            if (itemElement) {
                itemElement.remove();
            }
            updateTotalPrice(price);
        } else {
            console.error('Ошибка при удалении товара из корзины:', data.message || 'Неизвестная ошибка');
        }
    })
    .catch(error => {
        console.error('Ошибка при выполнении DELETE-запроса:', error);
    });
}
