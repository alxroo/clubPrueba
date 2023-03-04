const btnDelPost = document.querySelectorAll('#btnPostDelete')

btnDelPost.forEach(boton =>{
  boton.addEventListener('click',(e)=>{
    const atributo = boton.getAttribute('data-Atributo')
    e.preventDefault()
    console.log(atributo)
    Swal.fire({
      title: '¿Estas seguro de eliminar registro?',
      icon: 'warning',
      showCancelButton: true,
      confirmButtonColor: '#3085d6',
      cancelButtonColor: '#d33',
      confirmButtonText: 'Si eliminar',
      cancelButtonText: 'Cancelar'
    }).then((result) => {
      if (result.isConfirmed) {
        location.href = `/eliminarPost/${atributo}`;
      }
    })

  })
})

const btnDelFix = document.querySelectorAll('#btnDelFixture')

btnDelFix.forEach(boton =>{
  boton.addEventListener('click',(e)=>{
    const atributo = boton.getAttribute('data-Atributo')
    e.preventDefault()
    console.log(atributo)
    Swal.fire({
      title: '¿Estas seguro de eliminar registro?',
      icon: 'warning',
      showCancelButton: true,
      confirmButtonColor: '#3085d6',
      cancelButtonColor: '#d33',
      confirmButtonText: 'Si eliminar',
      cancelButtonText: 'Cancelar'
    }).then((result) => {
      if (result.isConfirmed) {
        location.href = `/deleteVersus/${atributo}`;
      }
    })

  })
})

const btnDelBlog = document.querySelectorAll('#btnBlogDelete')

btnDelBlog.forEach(boton =>{
  boton.addEventListener('click',(e)=>{
    const atributo = boton.getAttribute('data-Atributo')
    e.preventDefault()
    console.log(atributo)
    Swal.fire({
      title: '¿Estas seguro de eliminar registro?',
      icon: 'warning',
      showCancelButton: true,
      confirmButtonColor: '#3085d6',
      cancelButtonColor: '#d33',
      confirmButtonText: 'Si eliminar',
      cancelButtonText: 'Cancelar'
    }).then((result) => {
      if (result.isConfirmed) {
        location.href = `/deleteBlog/${atributo}`;
      }
    })

  })
})