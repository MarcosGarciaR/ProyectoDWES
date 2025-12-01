function eliminarPersona(dni){
    var x = confirm("¿Eliminar persona con DNI " + dni + " ?");
    if(x) 
        return true;
    else
        return false;
}