window.addEventListener('load', () => {
  Array.prototype.filter.call(forms, (form) => {
    form.addEventListener('submit', function (event) {
      if (form.checkValidity() === false) {
        event.preventDefault();
        event.stopPropagation();
      }

      form.classList.add('was-validated');
    }, false);
  });
}, false);

const forms = document.getElementsByClassName('validation-form');

// function signup(){
//     let userid = $('#userid').val()
//     let username = $('#username').val()
//     let password = $('#password').val()
//     let rePassword = $('#re_password').val()
//     console.log(userid, username, password, rePassword)
//     $.ajax({
//         type : "POST",
//         url : "user/signup",
//         data: {
//             userid : userid,
//             username : username,
//             password : password,
//             repassword : rePassword
//         },
//         success:function (response){
//             if(response['result'] == 'fail'){
//                 alert(response['msg'])
//             }else{
//                 location.href = '/login'
//             }
//         }
//     })
// }
