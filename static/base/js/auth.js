// route 
var rProsesLogin = server + "auth/login/proses";
var rToDashboard = server + "dashboard";
// vue object 
var appAuth = new Vue({
    el : '#divLogin',
    data : {

    },
    methods : {
        loginAtc : function()
        {
            let username = document.querySelector("#txtUsername").value;
            let password = document.querySelector("#txtPassword").value;
            let ds = {'username':username, 'password':password}
            $.post(rProsesLogin, ds, function(data){
                if(data.status === 'sukses'){
                    window.location.assign(rToDashboard);
                }else{
                    pesanUmumApp('warning', 'Gagal', 'Username / Password salah !!!');
                }
            });
        }
    }
});

// inisialisasi 
document.querySelector("#txtUsername").focus();

function pesanUmumApp(icon, title, text)
{
  Swal.fire({
    icon : icon,
    title : title,
    text : text
  });
}