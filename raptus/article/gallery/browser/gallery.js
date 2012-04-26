/**
 * @author Harald Frießnegger
 *
 * fixes urls for javascript galleries such as
 * Products.jsImagePopups or collective.prettyphoto
 *
 * for search engine optimization, the gallery viewlet links to
 * article/image1.jpg/view and this script changes the link
 * back to the actual url that shall be used in the popup/overlay
 *
 * make sure the script is inserted/run before the gallery's js-code
 */

(function($) {
    $(function() {
        $("a[data-popupurl]").each(function(){$(this).attr('href', $(this).data('popupurl'))})
    });
})(jQuery);


