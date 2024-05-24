import Modal from "/scripts/modal.js";

export default class Movie {
    constructor(title, description, year, rating, runtime, lb_url, jw_url, trailer_url, genres, countries, offers, directors) {
        this.title = title;
        this.description = description;
        this.year = year;
        this.rating = rating;
        this.runtime = runtime;
        this.lb_url = lb_url;
        this.jw_url = jw_url;
        this.trailer_url = trailer_url;
        this.genres = this.getListHTML(genres, "movie-genres-list");
        this.countries = this.getFlags(countries, "countries-list");
        // TODO: expose urls
        this.offers = this.getListHTML(offers.map(o => o.name), "movie-offers-list");
        this.directors = directors.map(d => d.name);
        this.cover_url = "img/movie_temp.jpg";
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

        // TODO: change for the dynamic image cover later
        const imageElem = `<img class="movie-image-cover" src=${this.cover_url} alt="Watch this space, cover is comming soon" />`;
        const cover = this.createMovieElemHTML('figure', 'movie-image', imageElem);
        
        // handle the case if trailer is not available
        if (this.trailer_url) {
            //the html character code is an arrow directed to the right
            const imgCaption = this.createMovieElemHTML("figcaption", "movie-image-caption", "Trailer &#10162;");
            cover.appendChild(imgCaption);

            cover.addEventListener("click", () => new Modal(this.title, this.trailer_url).fillInModal());
        }

        const offers = this.createListWithTitle("offers", this.offers);

        movieLeft.appendChild(cover);
        movieLeft.appendChild(offers);

        return movieLeft;
    }

    createRightSide() {
        const movieRight = document.createElement("div");
        movieRight.classList.add("movie-right");

        const info = this.createFullMovieInfo();

        movieRight.appendChild(info);

        return movieRight;
    }

    createFullMovieInfo() {
        const movieInfoContainer = document.createElement('div');
        movieInfoContainer.classList.add("movie-info");

        const title = this.createMovieElemText("h1", "movie-title", this.title);
        const year = this.createMovieElemText("h2", "movie-year", this.year);
        const director = this.createDirectorsList(this.directors);
        const rating = this.createMovieElemText("h3", "movie-rating", this.rating);
        const runtime = this.createMovieElemText("h4", "movie-runtime", this.runtime? `${this.runtime} min` : "");
        const description = this.createMovieElemText("p", "movie-description", this.description);
        const genres = this.createListWithTitle("genres", this.genres);
        const counries = this.createListWithTitle("countries", this.countries);
        const links = this.getLinks();

        movieInfoContainer.appendChild(title);
        movieInfoContainer.appendChild(year);
        movieInfoContainer.appendChild(director);
        movieInfoContainer.appendChild(rating);
        movieInfoContainer.appendChild(runtime);
        movieInfoContainer.appendChild(description);
        movieInfoContainer.appendChild(genres);
        movieInfoContainer.appendChild(counries);
        movieInfoContainer.appendChild(links);

        return movieInfoContainer;
    }

    createDirectorsList(names) {
        const container = document.createElement('h2');
        container.classList.add("movie-directors");

        if(names) {
            let dirNamesStr = names.map(String).join(', ');
            let result = `Directed by <span class="directors-names">${dirNamesStr}</span>`;
            container.innerHTML = result;
        }

        return container;
    }

    createListWithTitle(name, data) {
        const container = document.createElement('div');
        container.classList.add(name);

        const titleUpper = name.charAt(0).toUpperCase() + name.slice(1);

        if(data !== "") {
            const title = this.createMovieElemText("h3", `${name}-title`, `${titleUpper}:`);
            container.appendChild(title);
            container.appendChild(data);
        }

        return container;
    }

    // expects countries object that has name and flag fields, class  
    getFlags(countries, name) {
        let flags = "";

        if (countries.length == 0) {
            return flags;
        }

        const list = document.createElement("ul");
        list.classList.add(name);

        countries.map(({flag, name} = country) => {
            // &#127987; adds white flag symbol as a default flag
            flag = flag || "&#127987;";
            flags += `<li class="country-flag">${flag}<span class="country-name-tooltip">${name}</span></li>`;
        })
        list.innerHTML = flags;
        return list;
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
