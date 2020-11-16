let pageNumJson = 'placeholderForJinjaGeneration';

function setUpPageNumNavigation() {
    let pageNumElement = document.getElementById("pageNumClickable");
    let pageNum = pageNumElement.innerHTML;
    $(pageNumElement).popover({
        "html": true,
        "sanitize": false,
        content: function() {
            let form = $(`<form id="new-page-num-form"><label for="pagenum">Go to Page: </label><input type="text" style="width:4em;margin-left:1em;text-align:center" name="pagenum" value="${pageNum}"></form>`);
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
