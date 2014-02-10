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
     * Update <input hidden>'s value to match the selected text option.
     *
     * The <input hidden> is generally a database ID, and the user gets to
     * choose text labels that have a 1-to-1 correspondence with database IDs.
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
     * `ui` is an object with an `item` attribute that's of interest.
     *
     * `ui.item` is an JavaScript object, with `label` and `value`,
     *    and `pk` attributes, representing what the user selected.
     *    This is pulled from a remote JSON call.
     *
     *    The `value` is *not* used as the <input hidden> value
     *    because jQueryUI autocomplete attempts to rewrite the textbox
     *    with `value` if it is set. Instead a `pk` value is set, which
     *    jQueryUI ignores.
     */
    function updateHiddenValue(event, ui) {
        var $hidden = $(getHiddenInput(this.id));
        $hidden.val(ui.item.pk).trigger('change')
    }


    /**
     * Change the display widget to show dataItem.
     *
     * Rather than take the display widget, this function takes the display
     * widget's corresponding <input hidden> ID.
     *
     * dataItem is an Javascript data object (populated based on a remote JSON
     * request)
     */
    function setText(hiddenID, dataItem) {
        var $textbox = $("#" + hiddenID + "_text");
        var $selectize = $textbox[0].selectize;

        // selectize hides the <input text> behind a custom overlay.
        // The overlays only show option items that selectize gets from its
        // sources. In order to set the display from code, first the option
        // has to exist, then the display has to be set to that option

        // creates an option, or if the option already exists, does nothing
        $selectize.addOption(text);

        $selectize.setValue(text.pk);  // updates the label
    }


    /**
     * Update the UI widget to show the current <input hidden> value.
     *
     * hiddenID is the HTML 'id' attribute of the <input hidden> to show.
     * The UI widget to update is automatically selected based on hiddenID.
     *
     * The url parameter should point to a service that can give a label for a
     * specified ID. The query parameter `id` is added to the string and then
     * a get request is sent.
     */
    function updateOnChange(hiddenID, url) {
        $("#"+hiddenID).change(function() {

            // add the 'id' querystring parameter
            var glue = url.indexOf("&") >= 0 ? "?" : "&";
            var newID = $(this).val();
            var requestURL = url + glue + "id=" + newID;

            // request text for the new ID
            $.getJSON(requestURL, null, function(data, textStatus) {
                if(textStatus === "success") {
                    setText(hiddenID, data[0]);
                } else {
                    setText(hiddenID, textStatus);
                }
            });
        });
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


    /**
     * Inject an autocompleting textbox next to an <input hidden>
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
    return {
        activateWidget: function(hiddenID, url) {
            var $textfield = $makeTextInput(hiddenID);
            $textfield.selectize({
                valueField: 'pk',
                labelField: 'label',
                searchField: 'label',
                create: false,
                maxItems: 1,
                load: function(query, callback) {
                    if(!query.length) return callback;
                    $.ajax({
                        url: url + "&term=" + encodeURIComponent(query),
                        type: 'GET',
                        error: function() {
                            callback();
                        },
                        success: function(res) {
                            callback(res);
                        }
                    })
                }
            });

            updateOnChange(hiddenID, url);
            var $hiddenElem = $("#"+hiddenID);

            // if there's an initial value, load the text for it
            if($hiddenElem.val()) {
                $hiddenElem.trigger('change');
            }
        }
    }

})(jQuery);


jQuery(function() {
   window.SIMPLESELECT_ACTIVATORS = window.SIMPLESELECT_ACTIVATORS || [];
   jQuery.each(window.SIMPLESELECT_ACTIVATORS, function(i, activator) {
       activator();
   });
});
