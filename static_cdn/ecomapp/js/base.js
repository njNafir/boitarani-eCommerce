$(document).ready(function(){
	// Contact page related

	var contactForm = $('#contact-form')
	var contactFormMethod = contactForm.attr('method')
	var contactFormAction = contactForm.attr('action')

	function formSubmitting(subBut, defTex, doSubmit){
		if (doSubmit){
			subBut.addClass('disabled')
			subBut.html('<i class="fa fa-spin fa-spinner"></i> Sending...')
		}else{
			subBut.removeClass('disabled')
			subBut.html(defTex)
		}
	}

	contactForm.submit(function(event){
		event.preventDefault()
		var contactFormData = contactForm.serialize()
		var submitButton = contactForm.find('[type="submit"]')
		var submitButtonTxt = submitButton.text()
		// console.log(submitButtonTxt)
		
		formSubmitting(submitButton, '', true)
		
		$.ajax({
			url: contactFormAction,
			method: contactFormMethod,
			data: contactFormData,
			success: function(data){
				contactForm[0].reset()
				$.alert({
					title: 'Success',
					content: data.message,
					theme: 'modern'
				})
				setTimeout(function(){
					formSubmitting(submitButton, submitButtonTxt, false)
				}, 500)
			},
			error: function(errorData){
				// console.log(errorData)
				var errorMsgOb = errorData.responseJSON
				var msg = ''
				$.each(errorMsgOb, function(key, value){
					msg += key + ': ' + value[0].message + ',<br>'
				})
				$.alert({
					title: 'Ooops!',
					content: msg,
					theme: 'modern',
				})
				setTimeout(function(){
					formSubmitting(submitButton, submitButtonTxt, false)
				}, 500)
			},
		})
	})

	// Search related

	var searchForm = $('#search-form')
	var searchInput = searchForm.find('[name="search"]')
	var searchButton = searchForm.find('[type="submit"]')
	var typingTimer;
	var typingInterval = 1500

	searchForm.keyup(function(event){
		clearTimeout(typingTimer)
		typingTimer = setTimeout(searchAuto, typingInterval)
	})
	searchForm.keydown(function(event){
		clearTimeout(typingTimer)
	})
	function spinButton(){
		searchButton.addClass('disabled')
		searchButton.html('<i class="fa fa-spin fa-spinner"></i> Searching...')
	}
	function searchAuto(){
		spinButton()
		var inputVal = searchInput.val()
		window.location.href = '/search/product/?search=' + inputVal
	}

	// Cart related
	var cartUpdate = $('#cart-update-js').find('form')
	var submitSpan = cartUpdate.find('#submit-span')
	var itemCount = $('#navbar-wrapper').find('#item-count')
	// console.log(itemCount)
	cartUpdate.submit(function(event){
		event.preventDefault()
		// console.log('Not passing anithing')
		var $that = $(this)
		// var actionEndpoint = $that.attr('action')
		var actionEndpoint = $that.attr('data-endpoint')
		var httpMethod = $that.attr('method')
		var formData = $that.serialize()

		$.ajax({
			url: actionEndpoint,
			method: httpMethod,
			data: formData,

			success: function(data){
				// console.log('success')
				// console.log(data)
				// console.log(data.added)
				// console.log(data.removed)
				// console.log(submitSpan.html())
				if (data.added){
					submitSpan.html('<button type="submit" class="btn btn-outline-secondary my-2 my-sm-0 btn-block">Remove from cart</button>')
					if (data.user_ready){
						var appendData = '<div class="btn-group btn-block"><a href="http://127.0.0.1:8000/cart" class="btn btn-outline-primary btn-group-item">In Cart</a><a href="http://127.0.0.1:8000/account/purchase_library/" class="btn btn-outline-secondary btn-group-item">In Library</a></div>'
					}
					else{
						var appendData = '<div class="btn-group btn-block"><a href="http://127.0.0.1:8000/cart/" class="btn btn-outline-primary btn-group-item">In Cart</a>'
					}
					submitSpan.append(appendData)
				}else{
					submitSpan.html('<button type="submit" class="btn btn-outline-secondary my-2 my-sm-0 btn-block">Add to cart</button>')
				}
				itemCount.text(data.itemCount)
				if (window.location.href.indexOf('cart') != -1){
					refreshCart()
				}
			},
			error: function(errorData){
				$.alert({
					title: 'Ooops!',
					content: 'An error occured!',
				})
			}
		})
	})

	function refreshCart(){
		// console.log('All is well')
		var cartTable = $('.cart_product_list').find('.table')
		var cartBody = cartTable.find('.tbody')
		// cartBody.text('<h1>Complete</h1>')

		var refreshCartUrl = '/cart/api/view/';
		var refreshCartMethod = 'GET';
		var refreshCartData = {};

		$.ajax({
			url: refreshCartUrl,
			method: refreshCartMethod,
			data: refreshCartData,

			success: function(data){
				// console.log('success')
				var hiddenProductRemoveForm = $('.cart-product-remove-form')
				var currentWindow = window.location.href
				var product = cartBody.find('.product')
				var subtotal = cartBody.find('.subtotal')
				var total = cartBody.find('.total')
				if (data.products.length > 0){
					product.html('')
					i = data.products.length
					$.each(data.products, function(index, value){
						var newProductRemoveForm = hiddenProductRemoveForm.clone()
						newProductRemoveForm.css('display', 'block')
						newProductRemoveForm.find('.product_id').val(value.id)
						cartBody.prepend("<tr><td class='table_data'>" + i + "</td><td class='table_data'><a href='" + value.link + "' class='product_title'>" + value.name + "</a>" + newProductRemoveForm.html() + "</td><td class='table_data'>" + value.price + "</td></tr>")
						i --
					})
				}else{
					window.location.href = currentWindow
				}
				subtotal.text(data.subtotal)
				total.text(data.total)
			},
			error: function(errorData){
				$.alert({
					title: 'Ooops!',
					content: 'An error occured!',
					theme: 'modern',
				})
			}
		})
	}
})