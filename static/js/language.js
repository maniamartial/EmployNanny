
  
$(document).ready(function() {
  var languages = [
    "English",
    "Swahili",
    "Kikuyu",
    "Luhya",
    "Kalenjin",
    "Luo",
    "Kamba",
    "Kisii",
    "Meru",
    "Mijikenda",
    "Taita",
    "Pokomo",
    "Taveta",
    "Kuria",
    "Aembu",
    "Ambeere",
    "Wadawida-Watuweta",
    "Somali",
    "Borana",
    "Rendille",
    "Oromo",
    "Maasai",
    "Turkana",
    "Samburu",
    "Pokot",
    "Nandi",
    "Hindi",
    "Arabic",
    "Portuguese",
    "German",
    "French",
    "Spanish"
    // Add more Kenyan languages or other languages here
  ];

  var languageSuggestions = new Bloodhound({
    datumTokenizer: Bloodhound.tokenizers.whitespace,
    queryTokenizer: Bloodhound.tokenizers.whitespace,
    local: languages
  });

  $('.typeahead').tagsinput({
    typeaheadjs: {
      source: languageSuggestions.ttAdapter(),
      displayKey: function(item) {
        return item;
      }
    }
  });

  $('.typeahead').on('input', function() {
    var input = $(this);
    var suggestionsContainer = input.closest('.language-input-container').find('.language-suggestions');

    if (input.val().length > 0) {
      suggestionsContainer.empty();

      var suggestions = languageSuggestions.get(input.val());

      if (suggestions.length > 0) {
        suggestions.forEach(function(suggestion) {
          var listItem = $('<li></li>').text(suggestion);
          suggestionsContainer.append(listItem);
        });

        var inputOffset = input.offset();
        var inputHeight = input.outerHeight();

        suggestionsContainer.css({
          top: inputOffset.top + inputHeight,
          left: inputOffset.left,
          width: input.outerWidth()
        });

        suggestionsContainer.show();
      } else {
        suggestionsContainer.hide();
      }
    } else {
      suggestionsContainer.hide();
    }
  });

  $(document).on('click', '.language-suggestions li', function() {
    var selectedValue = $(this).text();
    var input = $(this).closest('.language-input-container').find('.typeahead');

    input.tagsinput('add', selectedValue);
    input.val('');
    input.closest('.language-input-container').find('.language-suggestions').hide();
  });

  $(document).on('click', function(e) {
    var target = $(e.target);

    if (!target.hasClass('typeahead')) {
      $('.language-suggestions').hide();
    }
  });
});
