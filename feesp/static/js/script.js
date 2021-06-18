var card = document.getElementById("card");
      
function openRegister(){
    card.style.transform = "rotateY(-180deg)";
  
    
}
function openLogin(){
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