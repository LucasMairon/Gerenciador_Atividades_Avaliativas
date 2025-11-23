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