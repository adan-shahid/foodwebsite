$(document).ready(function(){
    $('.add_to_cart').on('click', function(e){
        e.preventDefault();
 
//WHEN I CLICK ON ADD_TO_CART BUTTON, IT WILL TAKE ALL THIS DATA.
        food_id = $(this).attr('data-id');
        url = $(this).attr('data-url');
        data = {
            food_id: food_id,
        }
        
// WE ARE SENDING THAT 'food_id' TO OUR 'add_to_cart' view using the 
// AJAX request
        $.ajax({
            type: 'GET',
            url: url,
            data: data,
            success: function(response){
                console.log(response)
                $('#cart_counter').html(response.cart_counter['cart_count']);
                $('#qty-'+ food_id).html(response.qty);
            }
        })
    })

    // PLACE THE FOOD ITEM CART QUANTITY ON LOAD.
    $('.item_qty').each(function(){
        // taking the value of id
        var the_id = $(this).attr('id') 
        var qty = $(this).attr('data-qty') 
        $('#'+ the_id).html(qty)
        // $('#'+ the_id).html(response.cart_counter['cart_count']);
    })
});