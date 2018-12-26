function getCookie(cname) {
    var name = cname + "=";
    var decodedCookie = decodeURIComponent(document.cookie);
    var ca = decodedCookie.split(';');
    for(var i = 0; i <ca.length; i++) {
        var c = ca[i];
        while (c.charAt(0) == ' ') {
            c = c.substring(1);
        }
        if (c.indexOf(name) == 0) {
            return c.substring(name.length, c.length);
        }
    }
    return "";
}

function login(){
    nama = $('#nama').val();
    ktp = $('#ktp').val();
    console.log(nama)
    console.log(ktp)
    $.ajax({
        method: 'POST',
        url:'http://localhost:5000/login',
        beforeSend: function(req) {
            req.setRequestHeader("Content-Type", "application/json");

        },
        data: JSON.stringify({
            "nama": nama,
            "ktp": ktp
        }),
        success: function(res){
            alert("Login sukses!")
            document.cookie = `token=${res}`
            window.location = "/votedpr.html"
        },
        error: function(err){
            console.log(err)
        }
    })
}

function daftarcalondpr(){
    $.ajax({
        url: 'http://localhost:5000/tampilkancaleg',
        beforeSend: function(req){
            req.setRequestHeader("Content-Type", "application/json")
        },
        success: function(res){
            data = JSON.parse(res)

            data.forEach(data => {
                $('#daftarcalon').append(`<div class="card bg-dark text-white">
                <img class="card-img" src="asset/login.jpg" alt="Card image">
                <div class="card-img-overlay">
                    <h5 class="card-title text-warning">${data.nama}</h5>
                    <p class="card-text text-warning">Anggota dapil kecamatan xxx Partai Indonesia Ayo Bangkit Ayo Bangkit</p>
                    <a href="#" class="btn btn-primary">Pilih</a>
                </div>
                </div>`)
            })
        },
        error: function(err){
            alert(err)
        }
    })

}