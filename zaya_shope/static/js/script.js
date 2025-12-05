function add_address(){
    const add= document.getElementById("add_address").style.display="block";
}


function togglePassword() {
    const pw = document.getElementById("password");
    if (pw.type === "password") {
        pw.type = "text";
    } else {
        pw.type = "password";
    }
}