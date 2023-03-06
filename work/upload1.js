const url = 'process1.php';
const form = document.querySelector('form');
form.addEventListener('submit', e => {
    e.preventDefault();
    const file = document.querySelector('[type=file]').files[0];
    const formData = new FormData();
    formData.append('file', file);
    fetch(url, {
        method: 'POST',
        body: formData
    }).then(response => {
        return response.text();
    }).then(data => {
        console.log(data);
    });
});