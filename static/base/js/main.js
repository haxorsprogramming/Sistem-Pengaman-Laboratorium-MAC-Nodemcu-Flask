// vue object 
var appUtama = new Vue({
    el : "#divDashboard",
    delimiters: ['[[', ']]'],
    data : {
        judulPage : ''
    },
    methods : {
    }
});

renderPage('dashboard/beranda', 'Dashboard');

function renderPage(page, judulPage)
{
    $("#divUtama").html("Memuat ...");
    $("#divUtama").load(server + page);
    window.document.title = judulPage + " - AR Presensi";
    appUtama.judulPage = judulPage;
}

function pesanUmumApp(icon, title, text)
{
  Swal.fire({
    icon : icon,
    title : title,
    text : text
  });
}

function confirmQuest(icon, title, text, x)
{
    Swal.fire({
        title: title,
        text: text,
        icon: icon,
        showCancelButton: true,
        confirmButtonColor: "#3085d6",
        cancelButtonColor: "#d33",
        confirmButtonText: "Yes",
        cancelButtonText: "No",
    }).then((result) => {
        if (result.value) {
            x();
        }
    });
}