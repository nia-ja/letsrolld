export default class Movie {
    constructor(title, description, year, rating, runtime, lb_url, jw_url, genres, countries, offers, directors) {
        this.title = title;
        this.description = description;
        this.year = year;
        this.rating = rating;
        this.runtime = runtime;
        this.lb_url = lb_url;
        this.jw_url = jw_url;
        this.genres = this.getListHTML(genres, "movie-genres-list");
        this.countries = this.getListHTML(countries, "movie-countries-list");
        this.offers = this.getListHTML(offers, "movie-offers-list");
        this.directors = directors;
        this.cover_url = "img/movie_temp.jpg"
    }

    createFullMovie() {
        const movieEl = document.createElement("div");
        movieEl.classList.add("movie-card");

        const leftSide = this.createLeftSide();
        const rightSide = this.createRightSide();


        movieEl.appendChild(leftSide);
        movieEl.appendChild(rightSide);

        return movieEl;
    }

    createLeftSide() {
        const movieLeft = document.createElement("div");
        movieLeft.classList.add("movie-left");

        // change for the dynamic image cover later
        const cover = this.createMovieElemHTML('div', 'movie-image', `<img class="movie-image-cover" src=${this.cover_url} alt="Watch this space, cover is comming soon" />`);
        cover.addEventListener("click", this.openModal.bind(this));

        const offers = this.createListWithTitle("offers", this.offers);

        movieLeft.appendChild(cover);
        movieLeft.appendChild(offers);

        return movieLeft;
    }

    openModal(event) {
        console.log(this.title);
        // @todo: Implement modal functionality
        // will have a link to the trailer later -> embedded video in the modal window
    }

    createRightSide() {
        const movieRight = document.createElement("div");
        movieRight.classList.add("movie-right");

        const info = this.createFullMovieInfo();

        movieRight.appendChild(info);

        return movieRight;
    }

    
    createTrailer () {}
    
    createFullMovieInfo() {
        const movieInfoConteiner = document.createElement('div');
        movieInfoConteiner.classList.add("movie-info");
        
        const title = this.createMovieElemText("h1", "movie-title", this.title);
        const year = this.createMovieElemText("h2", "movie-year", this.year);
        const rating = this.createMovieElemText("h3", "movie-rating", this.rating);
        const runtime = this.createMovieElemText("h4", "movie-runtime",`${this.runtime} min`);
        const description = this.createMovieElemText("p", "movie-description", this.description);
        const genres = this.createListWithTitle("genres", this.genres);
        const counries = this.createListWithTitle("countries", this.countries);
        const links = this.getLinks();
        
        
        movieInfoConteiner.appendChild(title);
        movieInfoConteiner.appendChild(year);
        movieInfoConteiner.appendChild(rating);
        movieInfoConteiner.appendChild(runtime);
        movieInfoConteiner.appendChild(description);
        movieInfoConteiner.appendChild(genres);
        movieInfoConteiner.appendChild(counries);
        movieInfoConteiner.appendChild(links);
        
        return movieInfoConteiner;
    }

    createListWithTitle(name, data) {
        const conteiner = document.createElement('div');
        conteiner.classList.add(name);

        const titleUpper = name.charAt(0).toUpperCase() + name.slice(1);

        if(data !== "") {
            const title = this.createMovieElemText("h3", `${name}-title`, `${titleUpper}:`);
            conteiner.appendChild(title);
            conteiner.appendChild(data);
        }

        return conteiner;
    }

    getListHTML(arr, name) {
        let result = "";
        
        if (arr.length !== 0) {
            const list = document.createElement("ul");
            list.classList.add(name);
        
            for(let i=0; i<arr.length; i++) {
                result += `<li>${arr[i]}</li>`;
            }
            list.innerHTML = result;
            return list;
        } else {
            return result;
        }
    }

    getLinks() {
        const links_container = document.createElement("div");
        links_container.classList.add("links");

        console.log(this.lb_url);
        console.log(this.jw_url);

        if(this.lb_url) {
            const lb_button = this.createButtonElem(["btn", "btn--link"]);
            const lb_link = this.createLinkElem(this.lb_url, "letterboxd", "Letterboxd");
            lb_button.appendChild(lb_link);
            links_container.appendChild(lb_button);
        }

        if (this.jw_url) {
            const jw_button = this.createButtonElem(["btn", "btn--link"]);
            const jw_link = this.createLinkElem(this.jw_url, "just_watch", "JustWatch");
            jw_button.appendChild(jw_link);
            links_container.appendChild(jw_button);
        }

        return links_container;
    }

    // arg: list of strings with class names
    createButtonElem(classes) {
        const button = document.createElement("button");
        classes.forEach(c => {
            button.classList.add(c);
        })

        return button;
    }
    
    createLinkElem(link, name, linkText) {
        const linkElem = document.createElement('a');
        linkElem.setAttribute("href", link);
        linkElem.setAttribute("target", "_blank");
        linkElem.classList.add("movie-link");
        linkElem.classList.add(`movie-link-${name}`);
        linkElem.innerText = linkText;
        return linkElem;
    }

    createMovieElemText(tag, name, text) {
        const elem = document.createElement(tag);
        elem.classList.add(name);
        elem.innerText = text;
        return elem;
    }

    createMovieElemHTML(tag, name, htmlString) {
        const elem = document.createElement(tag);
        elem.className = name;
        elem.innerHTML = htmlString;
        return elem;
    }

}
