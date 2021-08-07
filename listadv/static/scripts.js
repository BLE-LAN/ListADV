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