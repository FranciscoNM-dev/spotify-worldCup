
//Función para aleatoriezar un array
function shuffle(arr) {
    return [...arr].sort(() => Math.random() - 0.5)
}

fetch('/images') // hace una petición HTTP a la URL que le paso. Como si la abriera desde el navegador
    .then(response => response.json()) //coge la respuesta (lo que hay en esa página) y lo pasa a json
    .then(images => {
        //console.log(images) //lo imprime en la consola del navegador. Como print de python pero en js
        //const tracks = document.querySelectorAll('.scroll-track') //busca los scroll-track del html
        //Hago 3 query selector porque uno va a la der, otro a la izq, otro a la der
        const trackRight1 = document.querySelector('.scroll-row:nth-child(1) .scroll-track-right')
        //busca scroll-track-right DENTRO DE el primer scroll-row. Ojo a ese sistema de jerarquía
        const trackLeft = document.querySelector('.scroll-row:nth-child(2) .scroll-track-left')
        const trackRight2 = document.querySelector('.scroll-row:nth-child(3) .scroll-track-right')
        const third = Math.floor(images.length / 3)
        const row1 = images.slice(0, third)
        const row2 = images.slice(third, third * 2)
        const row3 = images.slice(third * 2)
        row1.forEach(url => { //por cada url de row1 lo que vamos a hacer es
            const img = document.createElement('img') //crear la foto...
            img.src = url // ... a partir de la url...
            trackRight1.appendChild(img) // ... y añade la img creada como hijo de track[0] que es
                                       // un scroll-track, fíjate que los definí antes
        })
        row1.forEach(url => { //por cada url de row1 lo que vamos a hacer es
            const img = document.createElement('img') //crear la foto...
            img.src = url // ... a partir de la url...
            trackRight1.appendChild(img) // ... y añade la img creada como hijo de track[0] que es
                                       // un scroll-track, fíjate que los definí antes
        //------------------------------------------------------------------------------
        //DOS VECES?? POR QUÉ?? porque para el efecto que quiero, cada miembro de tracks tiene que
        //estar "duplicado". En el html de game fíjate en la transformación XTransform 50. Eso es, 
        //se mueve 50% y vuelve al principio. Si duplico la lista, al mover 50% "vuelve a empezar"
        //y no se notará cuando vuelva al principio, entiendes?
        //------------------------------------------------------------------------------
        })
        row2.forEach(url => { //LO MISMO PARA row2 y tracks[1]
            const img = document.createElement('img')
            img.src = url
            trackLeft.appendChild(img)
        })
        row2.forEach(url => { //LO MISMO PARA row2 y tracks[1]
            const img = document.createElement('img')
            img.src = url
            trackLeft.appendChild(img)
        })
        //------------------------------------------------------------------------------
        row3.forEach(url => { //Y TAMBIÉN PARA row3 y tracks[2]
            const img = document.createElement('img')
            img.src = url
            trackRight2.appendChild(img)
        })
        row3.forEach(url => { //Y TAMBIÉN PARA row3 y tracks[2]
            const img = document.createElement('img')
            img.src = url
            trackRight2.appendChild(img)
        })
        //------------------------------------------------------------------------------
    })