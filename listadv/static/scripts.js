function obtener_detalle(objButton) 
{
  let device_id = objButton.value
  let div_detalle = document.getElementById("contenidoDetalle");
  $.ajax({
      type: 'POST',
      url: '/mapa/lista/detalle/' + device_id,
      success: function (response) 
      {
        div_detalle.innerHTML = response
        div_detalle.hidden = false
      },
      error: function () { console.log(error) }
  }); 
}

function obtener_pagina(objLink) 
{
  let page = objLink.getAttribute('value')
  let devicestable = document.getElementById("devicestable");
  $.ajax({
      type: 'POST',
      url: '/mapa/lista/pagina/' + page,
      success: function (response)
      {
        devicestable.innerHTML = response
      },
      error: function () { console.log(error) }
  }); 
}