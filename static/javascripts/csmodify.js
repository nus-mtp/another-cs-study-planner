/****************************************************************/
/* =============== CS-MODIFY JAVASCRIPT FILE ================== */
/* This file serves as the central javascript source for all the*/
/* custom-defined animations or interactions on the page.       */
/****************************************************************/

/*
 * FUNCTIONS FOR SIDEBAR ANIMATIONS
 */

/* Set the width of the side navigation to 400px */
function openSidebar() {
    document.getElementById("sidebar").style.width = "400px";
}

/* Set the width of the side navigation to 0 */
function closeSidebar() {
    document.getElementById("sidebar").style.width = "0";
}

$(function () {
  $('[data-toggle="tooltip"]').tooltip();
})


/*
 * FUNCTIONS FOR SCROLLING TO TOP OF PAGE
 */

// Collapses the navbar on scroll
$(window).scroll(function() {
    if ($(".navbar").offset().top > 50) {
        $(".navbar-fixed-top").addClass("top-nav-collapse");
    } else {
        $(".navbar-fixed-top").removeClass("top-nav-collapse");
    }
});

// jQuery for page scrolling feature - requires jQuery Easing plugin
$(function() {
    $('a.page-scroll').bind('click', function(event) {
        var $anchor = $(this);
        $('html, body').stop().animate({
            scrollTop: $($anchor.attr('href')).offset().top
        }, 1500, 'easeInOutExpo');
        event.preventDefault();
    });
});


/*
 * FUNCTIONS FOR ENABLING SORTING FOR CERTAIN TABLES
 */

 $(document).ready(function() {
    /*
     * order: [column #, asc/desc],
     * where column # uses 0-based indexing
     * from left to right
    */
    $('#module-listing-table').DataTable( {
        "aaSorting": []
    } );

    $('#fixed-mounting-table').DataTable( {
        "aaSorting": []
    } );

    $('#tentative-mounting-table').DataTable( {
        "aaSorting": []
    } );

    $('#student-year-table').DataTable( {
        "aaSorting": []
    } );

    $('#modified-modules-table').DataTable( {
        "aaSorting": [ 0, "asc" ]
    } );

    $('#student-focus-area-table').DataTable( {
        "aaSorting": []
    } );

    $('#oversubscribed-modules-table').DataTable( {
        "order": [[ 3, "desc" ]]
    } );
     
    $('#common-module-table').DataTable( {
        aaSorting: []
    } );

    $('#non-overlap-table').DataTable( {
        aaSorting: [],
        "deferRender": true
    } );
} );