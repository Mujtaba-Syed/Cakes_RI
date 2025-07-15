document.addEventListener("DOMContentLoaded", function () {
    console.log('DOM loaded and parsed');

    fetch('/review/api/reviews/')
        .then(response => response.json())
        .then(data => {
            let carousel = document.getElementById('testimonial-carousel');
            carousel.innerHTML = "";

            let chunkSize = 3; // Show 3 reviews per slide
            for (let i = 0; i < data.length; i += chunkSize) {
                let reviewsChunk = data.slice(i, i + chunkSize);
                let isActive = i === 0 ? "active" : "";

                let reviewItems = reviewsChunk.map(review => {
                    let stars = '<span class="text-warning">' + "★".repeat(review.rating) + "☆".repeat(5 - review.rating) + '</span>';

                    return `
                        <div class="col-md-4 d-flex justify-content-center">
                            <div class="card bg-dark text-white border-inner p-4 shadow-sm" style="min-height: 250px; overflow: hidden; width: 90%;">
                                <div class="d-flex align-items-center mb-3">
                                    <img class="img-fluid flex-shrink-0 rounded-circle" src="${review.image ? review.image : '/static/default-avatar.jpg'}" style="width: 50px; height: 50px;">
                                    <div class="ps-3">
                                        <h6 class="text-primary text-uppercase mb-1">${review.name}</h6>
                                        <span class="text-light small">${review.profession ? review.profession : "Client"}</span>
                                    </div>
                                </div>
                                <p class="card-text small text-light" style="height: 80px; overflow: hidden;">${review.review}</p>
                                <p>${stars}</p>
                            </div>
                        </div>
                    `;
                }).join('');

                let carouselItem = `
                    <div class="carousel-item ${isActive}">
                        <div class="row justify-content-center px-2">
                            ${reviewItems}
                        </div>
                    </div>
                `;

                carousel.innerHTML += carouselItem;
            }
        })
        .catch(error => console.error('Error fetching reviews:', error));
});
