
    document.addEventListener('DOMContentLoaded', function() {
        loadProducts('Cakes');

        document.querySelectorAll('.nav-link').forEach(tab => {
            tab.addEventListener('click', function(event) {
                const category = event.target.getAttribute('data-category');
                loadProducts(category);
                // Hide search results when switching categories
                hideSearchResults();
            });
        });

        // Search functionality
        const searchBtn = document.getElementById('searchBtn');
        const searchInput = document.getElementById('searchInput');
        const clearSearchBtn = document.getElementById('clearSearch');

        searchBtn.addEventListener('click', function() {
            const query = searchInput.value.trim();
            if (query) {
                searchProducts(query);
            }
        });

        searchInput.addEventListener('keypress', function(e) {
            if (e.key === 'Enter') {
                const query = searchInput.value.trim();
                if (query) {
                    searchProducts(query);
                }
            }
        });

        clearSearchBtn.addEventListener('click', function() {
            clearSearch();
        });
    });

    function loadProducts(category) {
        fetch(`/product/api/get_all_products/?category=${category}`)
        .then(response => response.json())
            .then(data => {
                const container = document.querySelector(`#${category.toLowerCase()}`);
                
                if (!container) {
                    console.error('Container not found for category:', category);
                    return;
                }
                
                // Ensure container has proper Bootstrap classes
                if (!container.classList.contains('row')) {
                    container.classList.add('row');
                }
                if (!container.classList.contains('g-3')) {
                    container.classList.add('g-3');
                }
                
                
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
                        <div class="col-lg-3 col-md-4 col-sm-6 p-3">
                            <div class="card h-100">
                                <div class="product-image">
                                    <img src="${product.image}" class="card-img-top" alt="${product.name}">
                                </div>
                                <div class="card-body d-flex flex-column">
                                    <h5 class="card-title">${product.name}</h5>
                                    <p class="card-text flex-grow-1">${product.description}</p>
                                    <p class="card-text fw-bold">Rs ${product.price}</p>
                                    <a href="/product/redirect-to-whatsapp/?cake_name=${encodeURIComponent(product.name)}&cake_price=${encodeURIComponent(product.price)}&cake_type=${encodeURIComponent(category)}" class="btn btn-primary mt-auto">
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

    function searchProducts(query) {
        // Get the currently active category
        const activeTab = document.querySelector('.nav-link.active');
        const currentCategory = activeTab ? activeTab.getAttribute('data-category') : 'Cakes';
        
        fetch(`/product/api/search_products/?q=${encodeURIComponent(query)}&category=${currentCategory}`)
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    displaySearchResults(data.data, query, data.count, currentCategory);
                } else {
                    console.error('Search error:', data.message);
                    showSearchError(data.message);
                }
            })
            .catch(error => {
                console.error('Error searching products:', error);
                showSearchError('Search failed. Please try again.');
            });
    }

    function displaySearchResults(products, query, count, category) {
        const searchResults = document.getElementById('searchResults');
        const searchResultsContainer = document.getElementById('searchResultsContainer');
        const clearSearchBtn = document.getElementById('clearSearch');
        
        // Show search results and clear button
        searchResults.style.display = 'block';
        clearSearchBtn.style.display = 'inline-block';
        
        // Hide category tabs
        document.querySelector('.tab-class').style.display = 'none';
        
        // Hide all category product containers
        const allCategoryContainers = document.querySelectorAll('.tab-content .row');
        allCategoryContainers.forEach(container => {
            container.style.display = 'none';
        });
        
        // Create search results with proper Bootstrap row structure
        let searchContent = `
            <div class="col-12 mb-4">
                <div class="alert alert-info text-center">
                    <h4 class="mb-2">🔍 Search Results in ${category}</h4>
                    <p class="mb-0">Found <strong>${count}</strong> product(s) matching "<strong>${query}</strong>" in ${category}</p>
                </div>
            </div>
        `;
        
        if (products.length > 0) {
            products.forEach(product => {
                const productCard = `
                    <div class="col-lg-3 col-md-4 col-sm-6 p-3">
                        <div class="card h-100">
                            <div class="product-image">
                                <img src="${product.image}" class="card-img-top" alt="${product.name}">
                            </div>
                            <div class="card-body d-flex flex-column">
                                <h5 class="card-title">${product.name}</h5>
                                <p class="card-text flex-grow-1">${product.description}</p>
                                <p class="card-text fw-bold">Rs ${product.price}</p>
                                <a href="/product/redirect-to-whatsapp/?cake_name=${encodeURIComponent(product.name)}&cake_price=${encodeURIComponent(product.price)}&cake_type=${encodeURIComponent(product.category)}" class="btn btn-primary mt-auto">
                                    Order on WhatsApp
                                </a>
                            </div>
                        </div>
                    </div>
                `;
                searchContent += productCard;
            });
        } else {
            searchContent += `
                <div class="col-12 text-center">
                    <div class="alert alert-warning">
                        <h5>No products found</h5>
                        <p>Try searching with different keywords or browse our categories below.</p>
                    </div>
                </div>
            `;
        }
        
        searchResultsContainer.innerHTML = searchContent;
    }

    function clearSearch() {
        const searchInput = document.getElementById('searchInput');
        const searchResults = document.getElementById('searchResults');
        const searchResultsContainer = document.getElementById('searchResultsContainer');
        const clearSearchBtn = document.getElementById('clearSearch');
        const tabClass = document.querySelector('.tab-class');
        
        // Clear search input and hide results
        searchInput.value = '';
        searchResults.style.display = 'none';
        searchResultsContainer.innerHTML = '';
        clearSearchBtn.style.display = 'none';
        
        // Show category tabs again
        tabClass.style.display = 'block';
        
        // Show only the active category container
        const activeTab = document.querySelector('.nav-link.active');
        const currentCategory = activeTab ? activeTab.getAttribute('data-category') : 'Cakes';
        
        // Hide all category containers first
        const allCategoryContainers = document.querySelectorAll('.tab-content .row');
        allCategoryContainers.forEach(container => {
            container.style.display = 'none';
        });
        
        // Reset and reload products when clearing search to ensure proper structure
        resetAndLoadProducts(currentCategory);
    }

    function hideSearchResults() {
        const searchResults = document.getElementById('searchResults');
        const clearSearchBtn = document.getElementById('clearSearch');
        const tabClass = document.querySelector('.tab-class');
        
        searchResults.style.display = 'none';
        clearSearchBtn.style.display = 'none';
        tabClass.style.display = 'block';
        
        // Show only the active category container
        const activeTab = document.querySelector('.nav-link.active');
        const currentCategory = activeTab ? activeTab.getAttribute('data-category') : 'Cakes';
        
        // Hide all category containers first
        const allCategoryContainers = document.querySelectorAll('.tab-content .row');
        allCategoryContainers.forEach(container => {
            container.style.display = 'none';
        });
        
        // Reset and reload products when hiding search results
        resetAndLoadProducts(currentCategory);
    }

    function resetAndLoadProducts(category) {
        const container = document.querySelector(`#${category.toLowerCase()}`);
        
        if (!container) {
            console.error('Container not found for category:', category);
            return;
        }
        
        // Completely reset the container
        container.innerHTML = '';
        container.className = 'row g-3';
        container.style.display = 'block';
        
        // Now load products
        loadProducts(category);
    }

    function showSearchError(message) {
        const searchResults = document.getElementById('searchResults');
        searchResults.innerHTML = `
            <div class="col-12">
                <div class="alert alert-danger text-center">
                    <h5>Search Error</h5>
                    <p>${message}</p>
                </div>
            </div>
        `;
        searchResults.style.display = 'block';
    }
