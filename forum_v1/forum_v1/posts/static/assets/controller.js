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

function add_parameter(url, param, value){
    var hash       = {};
    var parser     = document.createElement('a');

    parser.href    = url;

    var parameters = parser.search.split(/\?|&/);

    for(var i=0; i < parameters.length; i++) {
        if(!parameters[i])
            continue;

        var ary      = parameters[i].split('=');
        hash[ary[0]] = ary[1];
    }

    hash[param] = value;

    var list = [];  
    Object.keys(hash).forEach(function (key) {
        list.push(key + '=' + hash[key]);
    });

    parser.search = '?' + list.join('&');
    return parser.href;
}

$("#search_bar").on("keydown", function(event) {
    // Get the value in the search bar.
    event.stopPropagation();
    if (event.which == 13) {
        search_for_text = $("#search_bar").val();
        window.location.href = add_parameter(window.location.href, "q", search_for_text)
    } 
});