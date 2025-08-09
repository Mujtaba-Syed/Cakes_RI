
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
                
                // Add pricing header based on category
                let pricingHeader = '';
                if (category === 'Cakes') {
                    pricingHeader = `
                        <div class="col-12 mb-4">
                            <div class="alert alert-info text-center">
                                <h4 class="mb-2">🎂 Cake Pricing</h4>
                                <small class="text-muted">Starting from</small>
                                <p class="mb-0"><strong>Rs 1600 per pound</strong></p>
                                <small class="text-muted">All our cakes are priced per pound. Contact us for custom sizes! (Minimum 2 pound)</small>
                            </div>
                        </div>
                    `;
                } else if (category === 'Cupcakes') {
                    pricingHeader = `
                        <div class="col-12 mb-4">
                            <div class="alert alert-info text-center">
                                <h4 class="mb-2">🧁 Cupcake Pricing</h4>
                                <small class="text-muted">Starting from</small>
                                <p class="mb-0"><strong>Rs 320 per piece</strong></p>
                                <small class="text-muted">Perfect for individual servings or bulk orders! (Minimum 6 pieces)</small>
                            </div>
                        </div>
                    `;
                } else if (category === 'Bouquets') {
                    pricingHeader = `
                        <div class="col-12 mb-4">
                            <div class="alert alert-info text-center">
                                <h4 class="mb-2">🌸 Bouquet Pricing</h4>
                                <small class="text-muted">Starting from</small>
                                <p class="mb-0"><strong>Rs 1800 per bouquet</strong></p>
                                <small class="text-muted">Contact us for custom designs and special orders!</small>
                            </div>
                        </div>
                    `;
                } else if (category === 'Cookies') {
                    pricingHeader = `
                        <div class="col-12 mb-4" >
                            <div class="alert alert-info text-center">
                                <h4 class="mb-2">🍪 Cookie Pricing</h4>
                                <small class="text-muted">Starting from</small>
                                <p class="mb-0"><strong>Rs 350 per piece</strong></p>
                                <small class="text-muted">Ideal for both personal treats and party platters. (Minimum 8 pieces)</small>
                            </div>
                        </div>
                    `;
                } else if (category === 'Customs') {
                    pricingHeader = `
                        <div class="col-12 mb-4">
                            <div class="alert alert-info text-center">
                                <h4 class="mb-2">🎨 Custom Orders</h4>
                                <p class="mb-0">We create unique designs tailored to your needs.</p>
                                <small class="text-muted">Contact us directly for personalized pricing and options.</small>
                            </div>
                        </div>
                    `;
                }
                
                // Add pricing header if it exists
                if (pricingHeader) {
                    container.innerHTML = pricingHeader;
                }
                
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
                                    <p class="card-text"> Rs ${product.price}</p>
                                    <a href="/product/redirect-to-whatsapp/?cake_name=${encodeURIComponent(product.name)}&cake_price=${encodeURIComponent(product.price)}&cake_type=${encodeURIComponent(category)}" class="btn btn-primary">
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
