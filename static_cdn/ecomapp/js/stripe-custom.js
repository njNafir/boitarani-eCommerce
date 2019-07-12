$(document).ready(function(){
  var stripePaymentForm = $('.stripe-payment-form')
  var stripePaymentFormAction = stripePaymentForm.attr('action')
  var stripePaymentFormDataToken = stripePaymentForm.attr('data-token')
  var stripePaymentFormDataBtnText = stripePaymentForm.attr('data-btn-title') || 'Add'
  var stripePaymentFormDataNextUrl = stripePaymentForm.attr('data-next-url')


  var stripePaymentFormTemplate = $.templates('#stripeTemplate')
  var stripePaymentFormTemplateContext = {
    action: stripePaymentFormAction,
    publish_key: stripePaymentFormDataToken,
    next_url: stripePaymentFormDataNextUrl,
    btn_text: stripePaymentFormDataBtnText
  }

  var stripePaymentFormTemplateWithAll = stripePaymentFormTemplate.render(stripePaymentFormTemplateContext)
  stripePaymentForm.html(stripePaymentFormTemplateWithAll)


  var paymentForm = $('#payment-form')
  var paymentFormDataToken = paymentForm.attr('data-token')
  var paymentFormDataNextUrl = paymentForm.attr('data-next-url')

  // Create a Stripe client.
  var stripe = Stripe('pk_test_anlrFgnL9wPHJiqF2FOs38jR007D6o2uXd');

  // Create an instance of Elements.
  var elements = stripe.elements();

  // Custom styling can be passed to options when creating an Element.
  // (Note that this demo uses a wider set of styles than the guide below.)
  var style = {
    base: {
      color: '#32325d',
      fontFamily: '"Helvetica Neue", Helvetica, sans-serif',
      fontSmoothing: 'antialiased',
      fontSize: '16px',
      '::placeholder': {
        color: '#aab7c4'
      }
    },
    invalid: {
      color: '#fa755a',
      iconColor: '#fa755a'
    }
  };

  // Create an instance of the card Element.
  var card = elements.create('card', {style: style});

  // Add an instance of the card Element into the `card-element` <div>.
  card.mount('#card-element');

  // Handle real-time validation errors from the card Element.
  card.addEventListener('change', function(event) {
    var displayError = document.getElementById('card-errors');
    if (event.error) {
      displayError.textContent = event.error.message;
    } else {
      displayError.textContent = '';
    }
  });

  // // Handle form submission.
  // var form = document.getElementById('payment-form');
  // form.addEventListener('submit', function(event) {
  //   event.preventDefault();

  //   stripe.createToken(card).then(function(result) {
  //     if (result.error) {
  //       // Inform the user if there was an error.
  //       var errorElement = document.getElementById('card-errors');
  //       errorElement.textContent = result.error.message;
  //     } else {
  //       // Send the token to your server.
  //       stripeTokenHandler(result.token);
  //     }
  //   });
  // });


  var form = $('#payment-form');
  var loadBtn = form.find('.btn-load')
  var loadBtnDefaultHtml = loadBtn.html()
  var loadBtnDefaultClass = loadBtn.attr('class')

  form.on('submit', function(event) {
    event.preventDefault();

    // var $that = $(this)
    // var loadBtn = $that.find('.btn-load')
    loadBtn.blur()
    var loadTime = 1500
    var currentTimeout;
    var errorHtml = "<i class='fas fa-exclamation-circle'></i> An error ocured."
    var errorClass = "btn btn-danger desabled my-4"
    var loadingHtml = "<i class='fa fa-spin fa-spinner'></i> Loading..."
    var loadingClass = "btn btn-success my-4"

    stripe.createToken(card).then(function(result) {
      if (result.error) {
        // Inform the user if there was an error.
        var errorElement = $('#card-errors');
        errorElement.textContent = result.error.message;
        currentTimeout = displayBtnStatus(loadBtn, errorClass, errorHtml, loadTime)
      } else {
        // Send the token to your server.
        currentTimeout = displayBtnStatus(loadBtn, loadingClass, loadingHtml, loadTime)
        stripeTokenHandler(result.token);
      }
    });
  });


function displayBtnStatus(element, newClass, newHtml, loadTime){
  // var defaultHtml = element.html()
  // var defaultClass = element.attr('class')

  element.html(newHtml)
  element.removeClass(loadBtnDefaultClass)
  element.addClass(newClass)

  return setTimeout(function(){
    element.html(loadBtnDefaultHtml)
    element.removeClass(newClass)
    element.addClass(loadBtnDefaultClass)
  }, loadTime)

}

  function setTimeOutFun(next_url, timeoffset){
    setTimeout(function(){
      if (next_url){
        window.location.href = next_url
      }
    }, timeoffset)
  }

  // Submit the form with the token ID.
  function stripeTokenHandler(token) {
    var next_url = paymentFormDataNextUrl
    var paymentFormDataEndpoint = '/payment/'
    var paymentFormMethod = 'POST'
    var paymentFormData = {
      'token': token
    }
    $.ajax({
      data: paymentFormData,
      url: paymentFormDataEndpoint,
      method: paymentFormMethod,
      success: function(data){
        var successMsg = data.message || 'Yeah... you are success...'
        if (next_url){
          successMsg = successMsg + "<br/><br/><i class='fa fa-spin fa-spinner'></i> Redirecting..."
        }
        card.clear()
        if ($.alert){
          $.alert(successMsg)
        }
        else{
          alert(successMsg)
        }
        loadBtn.html(loadBtnDefaultHtml)
        loadBtn.attr('class', loadBtnDefaultClass)
        setTimeOutFun(next_url, 320)
      },
      error: function(errorData){
        // console.log(errorData)
        if ($.alert){
          $.alert({title: 'An error ocured', content: 'Please try adding your card again.'})
        }
        else{
          alert('An error ocured <br/> Please try adding your card again.')
        }
        loadBtn.html(loadBtnDefaultHtml)
        loadBtn.attr('class', loadBtnDefaultClass)
      },
    })

    // Insert the token ID into the form so it gets submitted to the server
    // var form = document.getElementById('payment-form');
    // var hiddenInput = document.createElement('input');
    // hiddenInput.setAttribute('type', 'hidden');
    // hiddenInput.setAttribute('name', 'stripeToken');
    // hiddenInput.setAttribute('value', token.id);
    // form.appendChild(hiddenInput);

    // // Submit the form
    // form.submit();
  }
})