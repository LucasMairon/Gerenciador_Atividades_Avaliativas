function cleanAvailableList() {
    var selectedList = document.getElementById("selected-questions");
    var availableWrapper = document.getElementById("available-questions-wrapper");
    
    if (!selectedList || !availableWrapper) return;

    var selectedIds = Array.from(selectedList.querySelectorAll(".question-card"))
                           .map(card => card.dataset.questionId);

    var availableCards = availableWrapper.querySelectorAll(".question-card");
    availableCards.forEach(function(card) {
        if (selectedIds.includes(card.dataset.questionId)) {
            card.remove(); 
        }
    });
}

function initAvailableList() {
    var availableList = document.getElementById("available-questions");
    if (!availableList) return;

    new Sortable(availableList, {
        group: "shared-questions",
        animation: 0,
        sort: false,
        onEnd: function (evt) {
            checkPlaceholders();
        },
    });
}

function initSelectedList() {
    var selectedList = document.getElementById("selected-questions");
    if (!selectedList) return;

    new Sortable(selectedList, {
        group: "shared-questions",
        animation: 0,
        
        onAdd: function (evt) {
            var itemEl = evt.item;
            var newId = itemEl.dataset.questionId;
            
            var existingItems = selectedList.querySelectorAll(`[data-question-id="${newId}"]`);
            
            if (existingItems.length > 1) {
                itemEl.remove();
            }
            
            updateHiddenInput();
            checkPlaceholders();
        },

        onEnd: function (evt) {
            updateHiddenInput();
            checkPlaceholders();
        },
        onRemove: function (evt) {
             updateHiddenInput();
             checkPlaceholders();
        }
    });
}

function updateHiddenInput() {
    var selectedList = document.getElementById("selected-questions");
    var hiddenInput = document.getElementById("questions_ids_input");
    var questionCards = selectedList.querySelectorAll(".question-card");

    var ids = [];
    questionCards.forEach(function (card) {
        ids.push(card.dataset.questionId);
    });
    
    var uniqueIds = [...new Set(ids)];
    hiddenInput.value = uniqueIds.join(",");
}

function checkPlaceholders() {
    var selectedList = document.getElementById("selected-questions");
    var emptySelectedPlaceholder = document.getElementById("empty-selected-placeholder");

    if (selectedList && emptySelectedPlaceholder) {
        var selectedItems = selectedList.querySelectorAll(".question-card");

        if (selectedItems.length > 0) {
            emptySelectedPlaceholder.classList.add("d-none");
            emptySelectedPlaceholder.classList.remove("d-flex");
        } else {
            emptySelectedPlaceholder.classList.remove("d-none");
            emptySelectedPlaceholder.classList.add("d-flex");
        }
    }
}

document.addEventListener("DOMContentLoaded", function () {
    initAvailableList();
    initSelectedList();
    
    updateHiddenInput(); 
    cleanAvailableList();
    
    checkPlaceholders();
});

document.body.addEventListener("htmx:afterSwap", function (event) {
    if (event.detail.target.id === "available-questions-wrapper") {
        cleanAvailableList();
        initAvailableList();
        checkPlaceholders();
    }
});