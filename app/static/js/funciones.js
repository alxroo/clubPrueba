const btnDelTeam = document.querySelectorAll('#btnTeamDelete')

btnDelTeam.forEach(boton =>{
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
        location.href = `/deleteTeam/${atributo}`;
      }
    })

  })
})


