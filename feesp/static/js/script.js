var card = document.getElementById("card");
var mn=document.getElementById("mainx");
var cnt1=document.getElementById("logtext");
var cnt2=document.getElementById("regtext");
var element = document.getElementById("indv-ppt");

      
function openLogin(){
    card.style.transform = "rotateY(-180deg)";
    mn.classList.remove("excontainers");
    mn.classList.add("containers");
    cnt1.style.transform="translate(300%,-200%)";
    cnt2.style.transform="translate(-2200%,5000%)";   
   /* var src = element.getAttribute("data-one");
    element.setAttribute("src", src); */
}
function openRegister(){
   
    card.style.transform = "rotateY(0deg)";
    cnt1.style.transform="translate(2000%,-5000%)";
    cnt2.style.transform="translate(-330%,150%)";
    mn.classList.remove("containers");
    mn.classList.add("excontainers");
    /*var src = element.getAttribute("data-original");
    element.setAttribute("src", src);*/

}
/***********function for register password unmask */
function passVisible1() {
   var x=document.querySelectorAll(".passcode");
   x.forEach(element => {if (element.type === "password") {
    element.type = "text";
  } else {
    element.type = "password";
  }   
   });
  }
/***********function for login password unmask */
  function passVisible(){
      var x= document.querySelector(".passcode1")
      if (x.type === "password") {
        x.type = "text";
      } else {
        x.type = "password";
      }
  }
  function simpas(){
    var pass1=document.getElementById("pass");
    var pass2=document.getElementById("passc");
    if(pass1!=pass2)
    {
      pass2.setAttribute(ValidityState,false);
      pass2.textContent=" ";
    }
    else{
      pass2.setAttribute(ValidityState,true);
    }
  }
