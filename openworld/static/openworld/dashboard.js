/* AJAX pagination -- update links and table */
function ajax_get_update()
{
   $.get(url, function(results){
           console.log(results);
      var table = $("table", results);
      var span = $("span.step-links", results);

      $('#ajax_table_result').html(table);
      $('.step-links').html(span);
    }, "html");
}

/* AJAX -- loads an entry */
function loadEntry(url)
{
    $("#content").load( url );
}

/* AJAX -- loads the submit tags page */
var entry_id = '1';
function loadSubmitTags(url, entry_id)
{
    entry_id = entry_id;
    $("#content").load( url );
}

$( document ).ready( function() {
    /* AJAX -- load entries on start */
    $("#content").load( $( 'a.link#entries' ).attr('href') );

    /* AJAX pagination -- bind links to action  */
    var viewentries = $( 'a.link#entries' ).attr('href');

    $( '.step-links #prev' ).click( function(e) {
        e.preventDefault();
        url = viewentries + $( '.step-links #prev' ).attr('href');
        ajax_get_update();
    });
    $( '.step-links #next' ).click( function(e) {
        e.preventDefault();
        url = viewentries + $( '.step-links #next' ).attr('href');
        ajax_get_update();

    });
    
    /* AJAX -- links */
    $( 'a.link' ).click( function(e) {
        e.preventDefault();
        $("#content").load( this.href );
    });
});


/* AJAX pagination -- reload links */
$( document ).ajaxStop( function() {
    var viewentries = $( 'a.link#entries' ).attr('href');

    $( '.step-links #prev' ).click( function(e) {
        e.preventDefault();
        url = viewentries + $( '.step-links #prev' ).attr('href');
        ajax_get_update();
    });
    $( '.step-links #next' ).click( function(e) {
        e.preventDefault();
        url = viewentries + $( '.step-links #next' ).attr('href');
        ajax_get_update();
    });
});
