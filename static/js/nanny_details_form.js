document.addEventListener('DOMContentLoaded', function() {
  const languageInput = document.querySelector('.language-input');
  const languageOptions = document.querySelector('#language-options');

  languageInput.addEventListener('input', function() {
    const enteredValues = languageInput.value.split(',').map(value => value.trim().toLowerCase());
    const validValues = [];

    for (let option of languageOptions.options) {
      const optionValue = option.value.toLowerCase();
      if (enteredValues.includes(optionValue)) {
        validValues.push(optionValue);
      }
    }

    languageInput.value = validValues.join(', ');
  });
});
