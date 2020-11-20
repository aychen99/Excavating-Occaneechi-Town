$(document).ready(function() {
  $("[id^=carousel-zoom]").lightGallery({ /* loop: select elements with id:"carousel-zoom" */
    selector: 'a'
  });
  $("[id^=archaeology-images]").lightGallery({ /* loop: select elements with id:"carousel-zoom" */
  selector: 'a'
  });
});

function setUpModals() {
  let contents = document.getElementById("text-chapter-contents");
  let imgAnchors = contents.getElementsByClassName("a-img");
  let refAnchors = contents.getElementsByClassName("a-ref");
  let tableAnchors = contents.getElementsByClassName("a-table")
  let modalBody = document.getElementById("modal-body");
  let tableImgModalBody = document.getElementById("table-img-modal-body")
  for (let anchor of imgAnchors) {
    anchor.onclick = function(e) {
      modalBody.innerHTML = `
      <img src="${anchor.getAttribute("data-figure-path")}"></img>
      <br>
      <br>
      ${anchor.getAttribute("data-figure-caption")}`;
      modalBody.classList.add('img-modal-body');
      modalBody.classList.remove('ref-modal-body');
      modalBody.classList.remove('table-modal-body');
    }
  }
  for (let anchor of refAnchors) {
    anchor.onclick = function(e) {
      modalBody.innerHTML = `${anchor.getAttribute("data-author")}<br><p>${anchor.getAttribute("data-ref-text")}</p>`;
      modalBody.classList.add('ref-modal-body');
      modalBody.classList.remove('img-modal-body');
      modalBody.classList.remove('table-modal-body');
    }
  }
  for (let anchor of tableAnchors) {
    anchor.onclick = function(e) {
      modalBody.innerHTML = (`<p>${anchor.getAttribute("data-table-header")}</p>`
                             + `<pre>${anchor.getAttribute("data-table-string")}</pre>`);
      for (let tableImgAnchor of modalBody.getElementsByTagName("a")) {
        tableImgAnchor.onclick = function() {
          tableImgModalBody.innerHTML = `
          <img src="${tableImgAnchor.getAttribute("data-figure-path")}"></img>
          <br>
          <br>
          ${tableImgAnchor.getAttribute("data-figure-caption")}`;
        }
      }
      modalBody.classList.add('table-modal-body');
      modalBody.classList.remove('img-modal-body');
      modalBody.classList.remove('ref-modal-body');
    }
  }
};

setUpModals();
