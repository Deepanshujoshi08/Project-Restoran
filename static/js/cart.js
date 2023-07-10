
var updateBtns = $('.update-cart')

for(var i = 0; i < updateBtns.length; i++) {
 updateBtns[i].addEventListener('click', function(){
     var item_id = this.dataset.item;
     var action = this.dataset.action;
     console.log('product id: ', item_id, 'action: ', action)

     console.log('User :', user)
     if(user == 'AnonymousUser'){
         console.log('Not logged in')
     }else{
         updateUserCart(item_id, action)
     }
 })
}



function updateUserCart(item_id, action){
 console.log('User is logged in, sending data...')

 $.ajax({
     type: 'POST',
     url: '/update-cart/',
     headers: {
         'X-CSRFToken': csrftoken,
     },
     data: {
         'item': item_id,
         'act': action,
         
     },
     success: function (data) {
         data = JSON.parse(data)
         console.log( data.item, 'is added to cart', data.quantity, 'is added')
         location.reload();
     }

 })
 
}

