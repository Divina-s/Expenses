const usernameField=document.querySelector('#usernameField')
const feedBackArea=document.querySelector('.invalid_feedback')
const emailfield=document.querySelector('#emailfield')
const emailFeedBackArea=document.querySelector('.emailFeedBackArea')
const usernamesuccessOutput=document.querySelector('.usernamesuccessOutput')
const showPasswordToggle=document.querySelector('.showPasswordToggle' )
const passwordfield=document.querySelector('#passwordfield')
const submitBtn=document.querySelector('.submit-btn')

const handleToggleInput=(e) =>{
   if(showPasswordToggle.textContent==='SHOW'){
    showPasswordToggle.textContent='HIDE';
    passwordfield.setAttribute('type','text');
   } else{
    showPasswordToggle.textContent='SHOW'
    passwordfield.setAttribute('type','password');
   }

}

showPasswordToggle.addEventListener('click', handleToggleInput)


emailfield.addEventListener('keyup',(e) => {
    console.log('77777',77777);

    const emailVal=e.target.value;
   

    

    emailfield.classList.remove('is-invalid');
    emailFeedBackArea.style.display="none";
    
    
    if(emailVal.length >0){
      fetch('/validateemail/',{
      body:JSON.stringify({email: emailVal}), 
      method:'POST'
   })
     .then((res)=>res.json())
     .then((data)=> {
      console.log("data",data);
      if(data.email_error){
        
        submitBtn.disabled=true;
        emailfield.classList.add('is-invalid');
        emailFeedBackArea.style.display="block";
        emailFeedBackArea.innerHTML=`<p>${data.email_error}</p>`;
        
      }
      else{
        submitBtn.removeAttribute('disabled');
      }
   });
 }
});


usernameField.addEventListener('keyup',(e) => {
    console.log('77777',77777);

    const usernameVal=e.target.value;
    usernamesuccessOutput.style.display="block";
    usernamesuccessOutput.textContent='Checking ${usernameVal}';

    console.log('usernameVal', usernameVal);

    usernameField.classList.remove('is-invalid');
    feedBackArea.style.display="none";
    
    
    if(usernameVal.length >0){
      fetch('/validateusername/',{
      body:JSON.stringify({username: usernameVal}), 
      method:'POST'
   })
     .then((res)=>res.json())
     .then((data)=> {
      console.log("data",data);
      usernamesuccessOutput.style.display="none";
      if(data.username_error){
        submitBtn.disabled=true;
        usernameField.classList.add('is-invalid');
        feedBackArea.style.display="block";
        feedBackArea.innerHTML=`<p>${data.username_error}</p>`;
        
      }
      else{
        submitBtn.removeAttribute("disabled");
      }
   });
 }
});