window.onload=initAll
function initAll(){
  movei=0     
  movej=0
  movejAdd=1;
  window.setInterval(getwidth,50) //动态变更主页图片分辨率
  window.setInterval(changeImage,10000)  //每3秒图片变更一次
  downTitlePlots=document.getElementsByClassName("downTitle");
  imageContainers=document.getElementsByClassName("imageContainer");
  for (i=0;i<5;i++){
    downTitlePlots[i].onclick=clickDownPlots
  }
  //window.setInterval(scroll,10)  
}

//渐变效果
function changeImage(){
  var temp=document.getElementsByClassName("imageContainer");
  var temp2=document.getElementsByClassName("downTitle");
  var temp3=document.getElementsByClassName("streamerWord");
  
  //当前页面消失
  $(temp[movej]).fadeOut(1000);     //0123fadeOut

  //下一个页面显示
  $(temp[movejAdd]).fadeIn(1000);  
  
  //变更地下圆点的class
  temp2[movej].className="downTitle";
  temp2[movejAdd].className="downTitle active";
  
  //变更streamer
  temp3[movej].className="streamerWord";
  temp3[movejAdd].className="streamerWord streamerActive";

  movej=movejAdd;
  movejAdd=(movej+1)%5;
}

//点击后触发的渐变效果
function changeImage2(){
  var temp=document.getElementsByClassName("imageContainer");
  var temp2=document.getElementsByClassName("downTitle");
  var temp3=document.getElementsByClassName("streamerWord");
  
  //当前页面消失
  for(i=0;i<5;i++){
    $(temp[i]).fadeOut(1000);
  }
  //下一个页面显示
  $(temp[movej]).fadeIn(1000);  
  
  //变更地下圆点的class
  for(i=0;i<5;i++){
    temp2[i].className="downTitle";
  }
  temp2[movej].className="downTitle active";
  
  //变更streamer
  for(i=0;i<5;i++){
    temp3[i].className="streamerWord";
  }
  temp3[movej].className="streamerWord streamerActive";
  
  movej=movej;
  movejAdd=(movej+1)%5;
}

//通过检测浏览器的窗口来不断地更改图片的格式,从而保证图片的比例正确
function getwidth(){
  winWidth=0
	winWidth=window.innerWidth;
	winHeight=window.innerHeight;
	setImage();
}

function setImage(){
  var x=document.getElementsByClassName('indexBg');
  if (winWidth<(winHeight/9*16))
  {
    for(i=0;i<5;i++){
      x[i].style.height=(winHeight+'px');
      x[i].style.width=(winHeight/9*16+'px');
    }
  }
  else
  {
    for(i=0;i<5;i++){
      x[i].style.width=(winWidth+'px');
      x[i].style.height=(winWidth/16*9+'px');
    }
  }   
}

//点击按钮触发的函数
function clickDownPlots() {
  x=this.getAttribute("index"); //x=0,1,2,3
  //alert(x);
  x=x*1;
  temp=document.getElementsByClassName("downTitle active");
  temp[0].className="downTitle";
  //alert('全部更改好');
  var y=document.getElementsByClassName("downTitle");
  y[x].className="downTitle active";    //y有5个元素
  movej=x;    //movej = 0,1,2,3
  movejAdd=(movej+1)%5;
  changeImage2();
  return false;
}