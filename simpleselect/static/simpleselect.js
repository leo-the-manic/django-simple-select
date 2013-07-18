/**
 * Get the <input hidden> for the textbox with the given ID.
 *
 * textboxID should be a string.
 *
 * returns a DOM element
 */
window.simpleselect_getHiddenInput = function(textboxID) {
    // if you have a field with id "foo", the textbox gets the id "foo_text"
    var textboxTagRegex = /_text$/;
    var fieldID = textboxID.replace(textboxTagRegex, '');
    return $("#" + fieldID).get(0);
}


/**
 * Set the <input type="hidden"> to match the user's selection
 *
 * This is called after the user has chosen an autocomplete
 * suggestion.
 *
 * Args: see http://api.jqueryui.com/autocomplete/#event-select
 *   for full detail.
 *
 * `this` is the <input type="text"> which the user uses to enter
 *    their filter terms and select an option.
 *
 * `ui.item` is an JavaScript object, with `label` and `value`,
 *    and `pk` attributes, representing what the user selected.
 *    This is pulled from a remote JSON call.
 *
 *    The `value` is *not* used as the <input hidden> value
 *    because jQueryUI autocomplete attemps to rewrite the textbox
 *    with `value` if it is set. Instead a `pk` value is set, which
 *    jQueryUI ignores.
 */
window.simpleselect_updateHiddenValue = function(event, ui) {
    var $hidden = $(simpleselect_getHiddenInput(this.id));
    $hidden.val(ui.item.pk).trigger('change')
}


/**
 * Defaults sent to jQueryUI.autocomplete()
 */
window.simpleselect_defaultAutocompleteArgs = {
    select: window.simpleselect_updateHiddenValue
};


/**
 * Set the text of the entry box that's associated with the given hidden field.
 */
window.simpleselect_setText = function(hiddenID, text) {
    var $textbox = $("#" + hiddenID + "_text");
    $textbox.val(text);
}


/**
 * Listen to hidden events on the input and activate the text accordingly.
 */
window.simpleselect_updateOnChange = function(hiddenID, url) {
    $("#"+hiddenID).change(function() {
        var glue = url.indexOf("&") >= 0 ? "?" : "&";
        var newID = $(this).val();
        var requestURL = url + glue + "id=" + newID;
        $.getJSON(url, null, function(data, textStatus) {
            if(textStatus == "success") {
                simpleselect_setText(hiddenID, "Success");
            } else {
                simpleselect_setText(hiddenID, textStatus);
            }
        });
    });
}


/**
 * Inject an autcompleting textbox next to an <input hidden>
 *
 * This is meant to be called by JS code that is put in the
 * template automatically by the Python AutocompleteWidget class.
 *
 * Parameters
 * hiddenID (string): the ID of a hidden input
 * url (string): a service that gives autocomplete suggestions for
 *               this field
 *
 * Doesn't return anything.
 *
 */
window.simpleselect_activateWidget = function(hiddenID, url) {
    var $textfield = simpleselect_$makeTextInput(hiddenID);
    var args = $.extend({ source: url },
                        window.simpleselect_defaultAutocompleteArgs);
    $textfield.autocomplete(args);
    window.simpleselect_updateOnChange(hiddenID);
}


/**
 * Make a new text input to manipulate the choice ID.
 *
 * This does *not* actually activate jQueryUI on the input, it
 * just creates a new <input> with an ID of `hiddenID + '_text'`,
 * and injects it into the DOM after the target <input hidden>.
 *
 * It will have the CSS class "simpleselect-search".
 *
 * returns a jQuery object containing the created element.
 */
window.simpleselect_$makeTextInput = function(hiddenID) {
    var textfieldID = hiddenID + '_text'
    var $textElem = $('<input>', {type: 'text', id: textfieldID,
                                  "class": "simpleselect-search"});
    $("#" + hiddenID).after($textElem);
    return $textElem;
}
