

function viewImage(id,path_image) {
      var address='<img src={}>';
      document.getElementById(id).innerHTML=address.replace("{}",path_image);
}
