let peliculas=[]
let generos=[]
let mensaje=null
listarGeneros()


function validarPelicula(){
    if (document.getElementById("txtCodigo").value==""){
        mensaje="Debe ingresar código de la Película"
        return false;
    }else if(document.getElementById("txtTitulo").value==""){
        mensaje="Debe ingresar Título de la Película"
        return false;
    }else if(document.getElementById("txtProtagonista").value==""){
        mensaje="Debe ingresar el Protagonista de la Película"
        return false;
    }else if(document.getElementById('txtDuracion').value==""){
        mensaje="Debe ingresar la duración de la Película"
        return false;
    }else if(document.getElementById('cbGenero').value==""){
        mensaje="Debe seleccionar el género de la Película"
        return false;
    }else if(document.getElementById('txtResumen').value==""){
        mensaje="Debe ingresar un pequeño resumen de la Película"
        return false;
    }else{
        return true;
    }
}

function validarGenero(){
    if (document.getElementById("txtGenero").value==""){
        mensaje="Debe ingresar nombre del género"
        return false
    }
    else{
        return true;
    }
}
function listarPeliculas(){
    url = "/pelicula/"
    fetch(url, {
        method: "GET",
        headers: {
            "Content-Type": "application/json",
        }
    })
        .then(respuesta => respuesta.json())
        .then(resultado => {
            peliculas = resultado.peliculas
            console.log(peliculas)
            mostrarPeliculasTabla()
        })
        .catch(error => {
            console.error(error)
        })
}


function listarGeneros(){
    url = "/genero/"
    fetch(url, {
        method: "GET",
        headers: {
            "Content-Type": "application/json",
        }
    })
        .then(respuesta => respuesta.json())
        .then(resultado => {
            generos = resultado.generos
            console.log(generos)
        })
        .catch(error => {
            console.error(error)
        })
}


function mostrarPeliculasTabla(){
    let datos=""
   
    peliculas.forEach(pelicula => {
        datos += "<tr>"
        datos += "<td>" + pelicula.codigo + "</td>"
        datos += "<td>" + pelicula.titulo + "</td>"
        datos += "<td>" + pelicula.duracion + "</td>"
        datos += "<td>" + pelicula.protagonista + "</td>"
        let genero = obtenerGenero(pelicula.genero.$oid);        
        datos += "<td>" + genero + "</td>"
        datos += '<td class="text-center" style="font-size:3vh">' +
            '<i class="fa fa-edit text-warning" title="Editar"></i>' +
            '<i class="fa fa-trash text-danger" title="Eliminar"></i></td>'
        datos += '</tr>'
        
    });
    document.getElementById("datosPeliculas").innerHTML = datos

}

function obtenerGenero(id){
    let retorno=""
    for (let index = 0; index < generos.length; index++) {
        const genero = generos[index];        
        if (genero._id.$oid==id){
            retorno= genero.nombre
            break
        }        
    }
    return retorno

}


/**
 * Función que se encarga de hacer
 * una petición al backend para
 * agregar una película.
 */
// Función para enviar los datos del formulario de agregar
function agregarPelicula() {
    const formData = new FormData(document.getElementById('frmPelicula'));
    
    fetch('/pelicula/', {
        method: 'POST',
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        if (data.estado) {
            Swal.fire({
                title: 'Éxito',
                text: data.mensaje,
                icon: 'success'
            }).then(() => {
                window.location.href = '/peliculas/';
            });
        } else {
            Swal.fire({
                title: 'Error',
                text: data.mensaje,
                icon: 'error'
            });
        }
    })
    .catch(error => {
        Swal.fire({
            title: 'Error',
            text: 'Error al agregar la película: ' + error,
            icon: 'error'
        });
    });
}


/**
 * Función que se encarga de hacer
 * una petición al backend para
 * agregar un género.
 */
function agregarGenero(){
    if(validarGenero()){
        const genero = {
            nombre: document.getElementById('txtGenero').value 
        }
        const url= "/genero/"
        fetch(url, {
            method: "POST",
            body: JSON.stringify(genero),
            headers: {
                "Content-Type": "application/json",
            }
        })
        .then(respuesta => respuesta.json())
        .then(resultado => {       
            if (resultado.estado){
                location.href="/generos/"
            }else{
                swal.fire("Add Genero",resultado.mensaje,"warning")
            }
        })
        .catch(error => {
            console.error(error)
        })
    }else{
        swal.fire("Add Genero",mensaje,"warning")
    }
}


/**
 * Función que se encarga de hacer la
 * petición al servidor para actualizar
 * una película de acuerdo con su id
 * @param {*} id 
 */
// Función para enviar los datos del formulario de editar
function editarPelicula(id) {
    const formData = new FormData(document.getElementById('frmPelicula'));
    formData.append('id', id);
    
    fetch('/pelicula/', {
        method: 'PUT',
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        if (data.estado) {
            Swal.fire({
                title: 'Éxito',
                text: data.mensaje,
                icon: 'success'
            }).then(() => {
                window.location.href = '/peliculas/';
            });
        } else {
            Swal.fire({
                title: 'Error',
                text: data.mensaje,
                icon: 'error'
            });
        }
    })
    .catch(error => {
        Swal.fire({
            title: 'Error',
            text: 'Error al actualizar la película: ' + error,
            icon: 'error'
        });
    });
}

/**
 * Función que realiza la petición al servidor
 * para eliminar una película de acuerdo con su id
 * @param {*} id 
 */
function deletePelicula(id) {
    Swal.fire({
        title: "¿Está seguro de eliminar esta película?",
        text: "Esta acción no se puede deshacer",
        icon: "warning",
        showCancelButton: true,
        confirmButtonText: "Sí, eliminar",
        cancelButtonText: "Cancelar",
        confirmButtonColor: "#d33"
    }).then((result) => {
        if (result.isConfirmed) {
            const pelicula = { 
                id: id  // Asegúrate que el backend espera 'id' como clave
            };
            const url = "/pelicula/";
            fetch(url, {
                method: "DELETE",
                body: JSON.stringify(pelicula),
                headers: {
                    "Content-Type": "application/json",
                }
            })
            .then(respuesta => respuesta.json())
            .then(resultado => {
                if (resultado.estado) {
                    Swal.fire({
                        title: "Eliminada",
                        text: resultado.mensaje,
                        icon: "success"
                    }).then(() => {
                        location.reload();  // Recargar la página para ver cambios
                    });
                } else {
                    Swal.fire("Error", resultado.mensaje, "error");
                }
            })
            .catch(error => {
                console.error(error);
                Swal.fire("Error", "No se pudo eliminar la película", "error");
            });
        }
    });
}

// Agrega estas funciones al final de tu archivo app.js

function editarGenero(id) {
    const nuevoNombre = prompt("Ingrese el nuevo nombre del género:");
    if (nuevoNombre) {
        const genero = {
            id: id,
            nombre: nuevoNombre
        };
        const url = "/genero/";
        fetch(url, {
            method: "PUT",
            body: JSON.stringify(genero),
            headers: {
                "Content-Type": "application/json",
            }
        })
        .then(respuesta => respuesta.json())
        .then(resultado => {
            if (resultado.estado) {
                Swal.fire({
                    title: "Éxito",
                    text: resultado.mensaje,
                    icon: "success"
                }).then(() => {
                    location.reload();
                });
            } else {
                Swal.fire("Error", resultado.mensaje, "error");
            }
        })
        .catch(error => {
            console.error(error);
            Swal.fire("Error", "No se pudo actualizar el género", "error");
        });
    }
}

function eliminarGenero(id) {
    Swal.fire({
        title: "¿Está seguro de eliminar este género?",
        text: "Esta acción no se puede deshacer",
        icon: "warning",
        showCancelButton: true,
        confirmButtonText: "Sí, eliminar",
        cancelButtonText: "Cancelar",
        confirmButtonColor: "#d33"
    }).then((result) => {
        if (result.isConfirmed) {
            const genero = { id: id };
            const url = "/genero/";
            fetch(url, {
                method: "DELETE",
                body: JSON.stringify(genero),
                headers: {
                    "Content-Type": "application/json",
                }
            })
            .then(respuesta => respuesta.json())
            .then(resultado => {
                if (resultado.estado) {
                    Swal.fire({
                        title: "Eliminado",
                        text: resultado.mensaje,
                        icon: "success"
                    }).then(() => {
                        location.reload();
                    });
                } else {
                    Swal.fire("Error", resultado.mensaje, "error");
                }
            })
            .catch(error => {
                console.error(error);
                Swal.fire("Error", "No se pudo eliminar el género", "error");
            });
        }
    });
}