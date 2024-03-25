const uploadForm = document.querySelector('#uploadForm');
const img = document.querySelector('#img');
const colorsDiv = document.querySelector('#colors');
const colorBadgeTemplate = document.querySelector('#colorTemplate');
// FIXME(jftsang) Stop this placeholder template from showing up

uploadForm.addEventListener('submit', (event) => {
    event.preventDefault();

    img.src = URL.createObjectURL(event.target.photo.files[0]);
    // FIXME(jftsang) This should be hidden until a photo is selected

    const formData = new FormData(uploadForm);
    fetch('/analyze', {
        method: 'POST',
        body: formData
    }).then(
        response => response.json()
    ).then(data => {
        colorsDiv.replaceChildren();
        data.forEach(colorInfo => {
            const newNode = colorBadgeTemplate.cloneNode(true);
            newNode.hidden = false;
            colorsDiv.appendChild(newNode);
            newNode.querySelector('.dot').style.backgroundColor = colorInfo.color;
            newNode.querySelector('.badge').innerHTML += `${colorInfo.color.toUpperCase()} ${colorInfo.occurrence}`;
            console.log(colorInfo);
        })
    });
})
