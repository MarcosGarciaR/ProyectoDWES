function eliminarPersona(dni){
    var x = confirm("¿Eliminar persona con DNI " + dni + " ?");
    if(x) 
        return true;
    else
        return false;
}

function eliminarPerfil(username){
    var x = confirm("¿Eliminar el usuario " + username + " ?");
    if(x)
        return true;
    else
        return false;
}

function eliminarRecepcionista(salario){
    var x = confirm("¿Eliminar el usuario con salario " + salario + " ?");
    if(x)
        return true;
    else
        return false;
}