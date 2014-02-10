var SimpleSelect = (function($) {

    /**
     * Get the <input hidden> for the textbox with the given ID.
     *
     * textboxID should be a string.
     *
     * returns a DOM element
     */
    function getHiddenInput(textboxID) {
        // if you have a field with id "foo", the textbox gets the id "foo_text"
        var textboxTagRegex = /_text$/;
        var fieldID = textboxID.replace(textboxTagRegex, '');
        return $("#" + fieldID).get(0);
    }


    /**
     * Set the value of an <input hidden> when the user picks an option.
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
    function updateHiddenValue(event, ui) {
        var $hidden = $(getHiddenInput(this.id));
        $hidden.val(ui.item.pk).trigger('change')
    }


    /**
     * Defaults sent to jQueryUI.autocomplete()
     */
    var defaultAutocompleteArgs = {
        autoFocus: true,
        select: updateHiddenValue
    };


    /**
     * Set the value of the textbox that controls the given hidden field
     */
    function setText(hiddenID, text) {
        var $textbox = $("#" + hiddenID + "_text");
        $textbox.val(text);
    }


    /**
     * Listen to hidden events on the input and activate the text accordingly.
     */
    function updateOnChange(hiddenID, url) {
        $("#"+hiddenID).change(function() {
            var glue = url.indexOf("&") >= 0 ? "?" : "&";
            var newID = $(this).val();
            var requestURL = url + glue + "id=" + newID;
            $.getJSON(requestURL, null, function(data, textStatus) {
                if(textStatus === "success") {
                    setText(hiddenID, data[0].label);
                } else {
                    setText(hiddenID, textStatus);
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
     */
    function activateWidget(hiddenID, url) {
        var $textfield = $makeTextInput(hiddenID);
        var args = $.extend({source: url},
                            defaultAutocompleteArgs);
        $textfield.autocomplete(args);
        updateOnChange(hiddenID, url);
        var $hiddenElem = $("#"+hiddenID);

        // if there's an initial value, load the text for it
        if($hiddenElem.val()) {
            $hiddenElem.trigger('change');
        }
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
    function $makeTextInput(hiddenID) {
        var textfieldID = hiddenID + '_text'
        var $textElem = $('<input>', {type: 'text', id: textfieldID,
                                      "class": "simpleselect-search"});
        $("#" + hiddenID).after($textElem);
        return $textElem;
    }

    return {

        /**
         * Turn raw <input hidden>s into SimpleSelect-enabled text fields.
         */
        activate: function(activators) {
            $.each(activators, function(i, activator) {
                activator();
            });
        }
    }

})(jQuery);


jQuery(document).ready(function() {
    SimpleSelect.activate(SIMPLESELECT_ACTIVATORS);
});
