window.onload=initall;
function initall(){
  var temp=document.getElementsByClassName("exampleTitles").length;
  for (i=0;i<temp;i++){
    document.getElementsByClassName("exampleTitles")[i].onclick=slideReverse;
  }
}
function slideReverse(){//案例的滑动与否函数
  var temp=this.getAttribute('index');
  $(document.getElementsByClassName("exampleDetails")[temp]).slideToggle();
  return false;
}