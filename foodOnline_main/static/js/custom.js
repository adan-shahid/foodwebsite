$(document).ready(function(){
    $('.add_to_cart').on('click', function(e){
        e.preventDefault();
        
        food_id = $(this).attr('data-id');
        url = $(this).attr('data-url');
        
        $.ajax({
            type: 'GET',
            url: url,
        })
    })
});