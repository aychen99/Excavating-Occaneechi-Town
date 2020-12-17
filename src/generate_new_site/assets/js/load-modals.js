/* Script that loads table, reference, and video modals while also initializing
 * a LightGallery for each image.
 * Requires jQuery due to use of LightGallery.
 */

function setUpModals() {
  let contents = document.getElementById("text-chapter-contents");
  if (!contents) {
    return;
  }
  let refAnchors = contents.getElementsByClassName("a-ref");
  let tableAnchors = contents.getElementsByClassName("a-table");
  let videoAnchors = contents.getElementsByClassName("a-video");
  let modalBody = document.getElementById("modal-body");
  let tableImgModalBody = document.getElementById("table-img-modal-body");
  for (let anchor of refAnchors) {
    anchor.onclick = function(e) {
      modalBody.innerHTML = `${anchor.getAttribute("data-author")}<br><p>${anchor.getAttribute("data-ref-text")}</p>`;
      modalBody.classList.add('ref-modal-body');
      modalBody.classList.remove('img-modal-body');
      modalBody.classList.remove('table-modal-body');
    }
  }
  for (let anchor of tableAnchors) {
    // Insert table and set it to "display:none;" so LightGallery can work on any image links in a table
    let hiddenDiv = document.createElement("div");
    let tablePre = document.createElement("pre");
    tablePre.innerHTML = anchor.getAttribute("data-table-string");
    hiddenDiv.appendChild(tablePre);
    hiddenDiv.style.display = "none";
    document.body.appendChild(hiddenDiv);
    anchor.onclick = function(e) {
      modalBody.innerHTML = "";
      modalBody.innerHTML = `<p>${anchor.getAttribute("data-table-header")}</p>`;
      modalBody.appendChild(tablePre);
      modalBody.classList.add('table-modal-body');
      modalBody.classList.remove('img-modal-body');
      modalBody.classList.remove('ref-modal-body');
    };
  }
  for (let anchor of videoAnchors) {
    youTubeLink = anchor.getAttribute("data-figure-path");
    anchor.onclick = function(e) {
      modalBody.innerHTML = `
      <div class="embed-responsive embed-responsive-4by3">
        <iframe class="embed-responsive-item" src="${anchor.getAttribute("data-figure-path")}"
        webkitallowfullscreen mozallowfullscreen allowfullscreen></iframe>
      </div>
      <br>
      <p class="text-center">${anchor.getAttribute("data-figure-caption")}</p>
      `;
    };
  }
};

$(document).ready(function() {
  // Initialize any carousels (i.e. in Excavation context pages)
  $("[id^=carousel-zoom]").lightGallery({
    selector: 'a'
  });
  // Initialize any images in Archaeology Primer chapter text
  $("[id^=archaeology-images]").lightGallery({
    selector: 'a'
  });
  // Initialize images on pages 13, 14, and 23 of the Primer
  $("#changeable-image-table").lightGallery({
    selector: 'a'
  });
  // Initialize any image links in paragraphs of text
  $("[class^=a-img]").lightGallery({
    selector: 'this'
  });

  setUpModals();
  // Set up LightGallery for images in tables 3 and 4
  $("pre").lightGallery({
    selector: "a",
    exThumbImage: "data-thumbnail"
  });
  // Make LightGallery's opening hide the table modal
  $("pre").on("onBeforeOpen.lg", function(e) {
    $("#genModal").css("z-index", 1000);
  });
  $("pre").on("onCloseAfter.lg", function(e) {
    $("#genModal").css("z-index", "");
  });
});
