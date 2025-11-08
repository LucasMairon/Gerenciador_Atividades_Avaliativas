// Validação do Bootstrap5
(() => {
  "use strict";

  const forms = document.querySelectorAll(".needs-validation");

  Array.from(forms).forEach((form) => {
    form.addEventListener(
      "submit",
      (event) => {
        if (!form.checkValidity()) {
          event.preventDefault();
          event.stopPropagation();
        }

        form.classList.add("was-validated");
      },
      false
    );
  });
})();

function setupAlternativeRadioLogic() {
  const container = document.getElementById("alternativas-container");
  if (!container) return;

  const radioHandler = (event) => {
    if (
      event.target.type === "checkbox" &&
      event.target.name.endsWith("is_correct")
    ) {
      const checkboxes = container.querySelectorAll(
        'input[name$="is_correct"]'
      );

      checkboxes.forEach((cb) => {
        if (cb !== event.target) {
          cb.checked = false;
        }
      });

      event.target.checked = true;
    }
  };

  if (container.radioHandler) {
    container.removeEventListener("change", container.radioHandler);
  }

  container.addEventListener("change", radioHandler);
  container.radioHandler = radioHandler;
}

document.addEventListener("DOMContentLoaded", setupAlternativeRadioLogic);

document.body.addEventListener("htmx:afterSwap", function (evt) {
  if (evt.detail.target.id === "alternativas-container") {
    setupAlternativeRadioLogic();
  }
});

//drag-and-drop
function initSortable() {
  var availableList = document.getElementById("available-questions");
  var selectedList = document.getElementById("selected-questions");

  if (!availableList || !selectedList) {
    return;
  }

  new Sortable(availableList, {
    group: "shared-questions",
    animation: 150,
    onEnd: function (evt) {
      checkPlaceholders();
    },
  });

  new Sortable(selectedList, {
    group: "shared-questions",
    animation: 150,
    onEnd: function (evt) {
      updateHiddenInput();
      checkPlaceholders();
    },
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
  hiddenInput.value = ids.join(",");
}

function checkPlaceholders() {
  var selectedList = document.getElementById("selected-questions");
  var emptySelectedPlaceholder = document.getElementById(
    "empty-selected-placeholder"
  );

  if (selectedList && emptySelectedPlaceholder) {
    var selectedItems = selectedList.querySelectorAll(".question-card");

    if (selectedItems.length > 0) {
      emptySelectedPlaceholder.classList.add("d-none");
    } else {
      emptySelectedPlaceholder.classList.remove("d-none");
      emptySelectedPlaceholder.classList.add("d-flex");
    }
  }
}

document.addEventListener("DOMContentLoaded", function () {
  initSortable();
  checkPlaceholders();
});

document.body.addEventListener("htmx:afterSwap", function (event) {
  if (event.detail.target.id === "available-questions-wrapper") {
    initSortable();
    checkPlaceholders();
  }
});
