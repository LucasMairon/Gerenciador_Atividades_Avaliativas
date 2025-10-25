document.addEventListener('DOMContentLoaded', function() {
    const btnAdd = document.getElementById('btn-add-alternativa');
    const form = document.getElementById('main-form');
    const container = document.getElementById('alternativas-container');

    if (btnAdd && form && container) {
        btnAdd.addEventListener('click', function() {
            const alternativaHTML = `
                <div class="input-group mb-2">
                    <span class="input-group-text">E)</span>
                    <input type="text" class="form-control" name="alternativa_texto_5" placeholder="Digite a alternativa E" required>
                    <div class="input-group-text">
                        <input class="form-check-input mt-0" type="radio" name="alternativa_correta" value="5">
                    </div>
                    <button class="btn btn-outline-danger btn-delete-alternativa" type="button">
                        <i class="bi bi-trash"></i>
                    </button>
                </div>
            `;
            
            container.insertAdjacentHTML('beforeend', alternativaHTML);
            
            this.style.display = 'none';

            form.setAttribute('hx-post', '/question/create/objective/?extra_alternative=True');
        });
    }

    if (container && btnAdd && form) {
        container.addEventListener('click', function(event) {
            const deleteButton = event.target.closest('.btn-delete-alternativa');
            
            if (deleteButton) {
                deleteButton.closest('.input-group').remove();
                
                btnAdd.style.display = 'block';

                form.setAttribute('hx-post', '/question/create/objective');
            }
        });
    }

});