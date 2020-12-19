/* JavaScript that enables typing in a page number and navigating to that page.
 * Filled out with a map of page numbers to page paths during site generation.
 */

let pageNumJson = 'placeholderForJinjaGeneration';

function setUpPageNumNavigation() {
    let pageNumElement = document.getElementById("pageNumClickable");
    let pageNum = pageNumElement.innerHTML;
    $(pageNumElement).popover({
        html: true,
        sanitize: false,
        content: function() {
            let form = $(`<form id="new-page-num-form" style="text-align:center;"><div><label for="pagenum"><b>Go to Page: </b></label></div><div><input type="text" style="width:8em;text-align:center" name="pagenum" value="${pageNum}"></div></form>`);
            form.submit(function(e) {
                e.stopPropagation();
                e.preventDefault(); // Prevent refreshing page on form submit
                let newPageNum = form.find("input").val();
                if (!(newPageNum in pageNumJson)) {
                    alert("Did not find page " + newPageNum + " on this site!");
                    return;
                }
                newPagePath = "../" + pageNumJson[newPageNum];
                window.open(newPagePath, "_self");
            });
            return form;
        },
        container: "body"
    });
};

setUpPageNumNavigation();
