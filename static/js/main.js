document.addEventListener('DOMContentLoaded', function() {

    // ===== Star Rating =====
    const starInputs = document.querySelectorAll('.star-rating input');
    starInputs.forEach(input => {
        input.addEventListener('change', function() {
            document.getElementById('id_rating').value = this.value;
        });
    });

    // ===== Form Validation =====
    const forms = document.querySelectorAll('form[data-validate]');
    forms.forEach(form => {
        form.addEventListener('submit', function(e) {
            let valid = true;
            const required = form.querySelectorAll('[required]');
            required.forEach(field => {
                if (!field.value.trim()) {
                    valid = false;
                    field.style.borderColor = '#e74c3c';
                } else {
                    field.style.borderColor = '';
                }
            });

            // Check star rating
            const ratingInput = form.querySelector('#id_rating');
            if (ratingInput && (!ratingInput.value || ratingInput.value === '0')) {
                valid = false;
                const starWrapper = form.querySelector('.star-rating');
                if (starWrapper) starWrapper.style.outline = '2px solid #e74c3c';
            }

            if (!valid) {
                e.preventDefault();
                alert('Please fill in all required fields and select a rating.');
            }
        });
    });

    // ===== Auto-dismiss alerts =====
    const alerts = document.querySelectorAll('.alert');
    alerts.forEach(alert => {
        setTimeout(() => {
            alert.style.transition = 'opacity 0.5s';
            alert.style.opacity = '0';
            setTimeout(() => alert.remove(), 500);
        }, 4000);
    });

    // ===== Confirm delete =====
    const deleteForms = document.querySelectorAll('form[data-confirm]');
    deleteForms.forEach(form => {
        form.addEventListener('submit', function(e) {
            if (!confirm(form.dataset.confirm || 'Are you sure you want to delete this?')) {
                e.preventDefault();
            }
        });
    });
});
