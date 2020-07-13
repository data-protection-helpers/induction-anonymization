let move_slider1 = document.querySelector('input#slider1')
let move_slider2 = document.querySelector('input#slider2')

move_slider1.addEventListener('input', function (){document.getElementById("h_max").innerHTML = this.value });
move_slider2.addEventListener('input', function(){document.getElementById("h_mean").innerHTML = this.value });


function viewImage(id,path_image) {
      var address='<img src={}>';
      document.getElementById(id).innerHTML=address.replace("{}",path_image);
}
