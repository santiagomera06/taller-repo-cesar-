let peliculas=[]
let generos=[]

listarGeneros()
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
function agregarPelicula(){
    url = "/pelicula/"
    const pelicula={
        codigo: document.getElementById('txtCodigo').value,
        titulo: document.getElementById('txtTitulo').value,
        protagonista: document.getElementById('txtProtagonista').value,
        duracion: document.getElementById('txtDuracion').value,
        resumen: document.getElementById('txtResumen').value,
        genero: document.getElementById('cbGenero').value,
        foto:''
    }
    fetch(url, {
        method: "POST",
        body: JSON.stringify(pelicula),
        headers: {
            "Content-Type": "application/json",
        }
    })
    .then(respuesta => respuesta.json())
    .then(resultado => {
        if (resultado.estado) {
           location.href = "/peliculas/"
        }else{
            swal.fire("Agregar Pelicula", resultado.mensaje, "warning")
        }
    })
        .catch(error => {
            console.error(error)
    })
}


/**
 * Función que se encarga de hacer
 * una petición al backend para
 * agregar un género.
 */
function agregarGenero(){
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
            swal.fire("Agregar Genero",resultado.mensaje,"warning")
        }
    })
    .catch(error => {
        console.error(error)
    })
}