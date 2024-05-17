const showMoviesButton = document.getElementById("movies-number");
const inputMoviesButton = document.getElementById("f_number");

showMoviesButton.addEventListener("click", e => {
    // e.preventDefault();
    const querryValue = inputMoviesButton.value;
    // console.log(typeof querryValue) // string
    if (querryValue !== "" && querryValue !== "0" && Number(querryValue)%3 === 0) {
        localStorage.setItem("querry_value", querryValue);
    }
});
