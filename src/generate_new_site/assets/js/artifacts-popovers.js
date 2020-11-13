function setUpPopovers() {
    let figurePopovers = $(".figure-popover");
    let detailsPopovers = $(".details-popover");

    figurePopovers.popover({
        html: true,
        sanitize: false,
        title: '<span class="text-secondary">Details</span>'+
        '<button type="button" id="close" class="close" onclick="$(&quot;.figure-popover&quot;).popover(&quot;hide&quot;);">&times;</button>',
        content: function() {
            return `<img src="${this.getAttribute("data-figure-path")}"></img>
                    <br>
                    <br>
                    ${this.getAttribute("data-figure-caption")}`;
        },
        placement: "bottom",
        container: "body"
        // fallbackPlacement: "flip"
    });

    detailsPopovers.popover({
        html: true,
        sanitize: false,
        title: '<span class="text-secondary">Details</span>'+
        '<button type="button" id="close" class="close" onclick="$(&quot;.details-popover&quot;).popover(&quot;hide&quot;);">&times;</button>',
        content: function() {
            return this.getAttribute("data-details-html");
        },
        placement: "bottom",
        container: "body"
    });
    
    /*$('[data-toggle="popover"]').popover({
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
    });*/
};

setUpPopovers();
