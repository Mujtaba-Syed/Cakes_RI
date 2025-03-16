
    document.addEventListener('DOMContentLoaded', function() {
        loadProducts('Cakes');

        document.querySelectorAll('.nav-link').forEach(tab => {
            tab.addEventListener('click', function(event) {
                const category = event.target.getAttribute('data-category');
                loadProducts(category);
            });
        });
    });

    function loadProducts(category) {
        fetch(`/product/api/get_all_products/?category=${category}`)
        .then(response => response.json())
            .then(data => {
                const container = document.querySelector(`#tab-${category.toLowerCase()} .row`);
                container.innerHTML = '';  
                data.forEach(product => {
                    const productCard = `
                        <div class="col-lg-3 p-3">
                            <div class="card">
                                <div class="product-image">
                                    <img src="${product.image}" class="card-img-top" alt="${product.name}">
                                </div>
                                <div class="card-body">
                                    <h5 class="card-title">${product.name}</h5>
                                    <p class="card-text">${product.description}</p>
                                    <p class="card-text">(Starting from) Rs ${product.price}</p>
                                    <a href="/product/redirect-to-whatsapp/?cake_name=${encodeURIComponent(product.name)}&cake_price=${encodeURIComponent(product.price)}&cake_desc=${encodeURIComponent(product.description)}&cake_type=${encodeURIComponent(category)}" class="btn btn-primary">
                                        Order on WhatsApp
                                    </a>
                                </div>
                            </div>
                        </div>
                    `;
                    container.innerHTML += productCard;
                });
            })
            .catch(error => console.error('Error fetching products:', error));
    }
