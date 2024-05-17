export default class Modal {
    // @todo: will need to add trailer url later
    constructor(title) {
        this.title = title;
        // this.url = url;
    }

    fillInModal() {
        const title = document.querySelector(".modal-title");
        title.textContent = this.title;

        // @todo: will have a dynamic link to the trailer later
        const body = document.querySelector(".modal-body");
        const trailer = this.createTrailer("https://www.youtube.com/embed/LtNYaH61dXY?si=j-aoQsvgBPQFIfBg");
        body.appendChild(trailer);

        this.openModal();

        const closeBtn = document.querySelector(".closeBtn");
        closeBtn.addEventListener("click", this.closeModal.bind(this));

        window.addEventListener('click', (e) => this.closeModalOutside(e));
    }

    createTrailer (url) {
        const trailer = document.createElement("iframe");
        trailer.setAttribute("width", "100%");
        trailer.setAttribute("height", "100%");
        trailer.setAttribute("src", url);
        trailer.setAttribute("title", this.title);
        trailer.setAttribute("frameborder", "0");
        trailer.setAttribute("allowfullscreen", true);
        trailer.setAttribute("referrerpolicy", "strict-origin-when-cross-origin");

        return trailer;
    }

    openModal() {
        const modal = document.getElementById("modal");
        modal.style.display = "block";
    }

    closeModal() {
        const modal = document.getElementById("modal");
        modal.classList.toggle("show-modal");
        modal.style.display = "none";
        this.stopVideos();
    }

    closeModalOutside(e) {
        const targetElem = e.target.getAttribute("class");
        const modalItem = document.getElementById("modal");
        console.log(targetElem);
        if(targetElem === "modal") {
            modalItem.style.display = "none";
            this.stopVideos();
        }
    }

    stopVideos() {
        const trailers = document.querySelectorAll("iframe");
        trailers.forEach(trailer => {
            trailer.src = "";
            trailer.remove();
        })
    }
}