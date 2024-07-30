// static/js/delete_item.js

function getCsrfToken() {
    return document.querySelector('meta[name="csrf-token"]').getAttribute('content');
}

function deleteItem(url, article) {
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
            const itemElement = document.getElementById(`item-${article}`);
            if (itemElement) {
                itemElement.remove();
            }
            console.log('Item successfully deleted:', article);
            return { success: true };
        }
        return response.json();
    })
    .then(data => {
        console.log('Response data:', data);
        if (!data.success) {
            console.error('Error deleting item:', data.message || 'Unknown error');
        }
    })
    .catch(error => {
        console.error('Error making DELETE request:', error);
    });
}