$(".filter").click(
    function() {
        var id = $(this).attr('id');
        current_location = window.location.pathname
        path_strs = current_location.split("/").filter(n => n)
        if (path_strs[path_strs.length - 1] == "posts") {
            path_strs.push(id)
        } else {
            path_strs.pop()
            path_strs.push(id)
        }
        new_location = path_strs.join("/")
        window.location.pathname = "/" + new_location
    }
);

$("#search_bar").on("input", function(event) {
    // Get the value in the search bar.
    event.stopPropagation();
    search_for_text = $("#search_bar").val();
    alert(search_for_text);
});