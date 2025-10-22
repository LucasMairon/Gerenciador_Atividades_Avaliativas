document.addEventListener('DOMContentLoaded', function() {

    const selectDisciplina = document.getElementById('select-disciplina');
    if (selectDisciplina) {
        $(selectDisciplina).select2({
            theme: "bootstrap-5",
            language: "pt-BR",
            placeholder: "Selecione a disciplina",
        });
    }
});