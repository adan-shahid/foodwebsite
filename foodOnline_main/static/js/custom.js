

$(document).ready(function(){
    // ADD TO CART 
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
               if (response.status == 'login_required'){
                    swal.fire({
                        title: "Not logged In",
                        text: response.message,
                        icon: "info"
                        }).then(function(){
                            window.location = '/login';
                        });
                    // console.log('Rasie the error messge')
                } else if(response.status == 'failed'){
                    swal.fire({
                        title: "Failed status",
                        text: response.message,
                        icon: "error"
                        });
                }
                else{
                    // FOR REAL TIME LOADING OF FOOD QUANTITY IN BOTH LOCATIONS
                    $('#cart_counter').html(response.cart_counter['cart_count']);
                    $('#qty-'+ food_id).html(response.qty);
                }
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

// DECREASE CART 
      $('.decrease_cart').on('click', function(e){
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
                // console.log(response)
               if (response.status == 'login_required'){
                    swal.fire({
                        title: "Not logged In",
                        text: response.message,
                        icon: "info"
                        }).then(function(){
                            window.location = '/login';
                        });
                    // console.log('Rasie the error messge')
                } else if(response.status == 'failed'){
                    swal.fire({
                        title: "Failed status",
                        text: response.message,
                        icon: "error"
                        });
                }else{

                    // FOR REAL TIME LOADING OF FOOD QUANTITY IN BOTH LOCATIONS
                    $('#cart_counter').html(response.cart_counter['cart_count']);
                    $('#qty-'+ food_id).html(response.qty);
                }
                // FOR REAL TIME LOADING OF FOOD QUANTITY IN BOTH LOCATIONS
                // $('#cart_counter').html(response.cart_counter['cart_count']);
                // $('#qty-'+ food_id).html(response.qty);
                
            }
        })
    })
});