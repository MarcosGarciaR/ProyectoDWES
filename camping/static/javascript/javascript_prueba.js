function eliminarPersona(dni){
    var x = confirm("¿Eliminar persona con DNI " + dni + " ?");
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

function eliminarCamping(nombre){
    var x = confirm("¿Eliminar el camping con nombre " + nombre + " ?");
    if(x)
        return true;
    else
        return false;
}

function eliminarParcela(numero){
    var x = confirm("¿Eliminar el camping con numero " + numero + " ?");
    if(x)
        return true;
    else
        return false;
}

function eliminarFactura(numero){
    var x = confirm("¿Eliminar la factura emitida en " + emitida_en + " ?");
    if(x)
        return true;
    else
        return false;
}