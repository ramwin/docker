window.onload = initall
function initall(){
  var temp=document.getElementsByClassName("EmployDetail").length;
  for (i=0;i<temp;i++){
    document.getElementsByClassName("EmployDetail")[i].onclick=slideReverse;
  }
}
function slideReverse(){//案例的滑动与否函数
  var temp=this.getAttribute('index');
  $(document.getElementsByClassName("EmployDetails")[temp]).slideToggle();
  return false;
}
