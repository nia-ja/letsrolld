import Movie from "/scripts/movie.js";
// import getQuerryNumber from "/scripts/button.js";

const button = document.getElementById("get")
const resContainer = document.getElementById("response")

button.addEventListener("click", getMovies)
window.onload = function() {
    getMovies();
}

async function getMovies() {
    const config = {
        headers: {
            Accept: "application/json",
        },
    }

    let querryValue = Number(window.localStorage.getItem("querry_value")) || 12;
    
    // default value shown in the form's input
    const moviesInput = document.getElementById("f_number");
    moviesInput.setAttribute("value", querryValue);

    
    const res = await fetch(`http://localhost:8000/films?limit=${querryValue}`, config)

    const data = await res.json()

    cleanUp()
    showMovies(data)
    window.scrollTo(0, 0);
}

function showMovies(movies) {
    movies.forEach(movie => {
        const {title, description, year, rating, runtime, lb_url, jw_url, genres, countries, offers, directors} = movie

        let movieEl = new Movie(title, description, year, rating, runtime, lb_url, jw_url, genres, countries, offers, directors);

        movieEl = movieEl.createFullMovie();

        resContainer.appendChild(movieEl);
    })
}

function cleanUp() {
    resContainer.innerHTML = "";
}