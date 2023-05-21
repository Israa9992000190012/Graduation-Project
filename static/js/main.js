/**** search button *******/
let searchForm = document.querySelector('.search-form');
document.querySelector('#search-btn').onclick = () => {
    searchForm.classList.toggle('active')
    shoppingCart.classList.remove('active')
    loginForm.classList.remove('active')
    navbar.classList.remove('active')

}

/**** shopping button *******/
let shoppingCart = document.querySelector('.shopping-cart');
document.querySelector('#cart-btn').onclick = () => {
    shoppingCart.classList.toggle('active')
    searchForm.classList.remove('active')
    loginForm.classList.remove('active')
    navbar.classList.remove('active')

}

/**** login button *******/
let menuBtn = document.querySelector('#menu-btn');
let loginForm = document.querySelector('.login-form');
document.querySelector('#login-btn').onclick = () => {
    loginForm.classList.toggle('active')
    searchForm.classList.remove('active')
    shoppingCart.classList.remove('active')
    navbar.classList.remove('active')
}



/**** menu button *******/
let navbar = document.querySelector('.navbar');
document.querySelector('#menu-btn').onclick = () => {
    navbar.classList.toggle('active')
    searchForm.classList.remove('active')
    shoppingCart.classList.remove('active')
    loginForm.classList.remove('active')

}



window.onscroll = () => {
    searchForm.classList.remove('active')
    shoppingCart.classList.remove('active')
    loginForm.classList.remove('active')
    navbar.classList.remove('active')
}


/************* men ****************/
document.querySelector('#shirt').addEventListener('click', () => {
    window.location.href = 'menTshirt.html';
});
document.querySelector('#shoes').addEventListener('click', () => {
    window.location.href = '';
});
document.querySelector('#trouser').addEventListener('click', () => {
    window.location.href = '';
});