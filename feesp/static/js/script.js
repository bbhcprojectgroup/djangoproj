var card = document.getElementById("card");
      
function openLogin(){
    card.style.transform = "rotateY(-180deg)";
  
    
}
function openRegister(){
    card.style.transform = "rotateY(0deg)";
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

  