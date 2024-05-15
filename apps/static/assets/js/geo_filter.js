
$(document).ready(function () {
    var person_org_tags = [];
    function findGetParameter(parameterName) {
        var result = null,
            tmp = [];
        location.search
            .substr(1)
            .split("&")
            .forEach(function (item) {
              tmp = item.split("=");
              if (tmp[0] === parameterName) result = decodeURIComponent(tmp[1]);
            });
        return result;
    }

    if (findGetParameter("date_start")) {
        $("#date-filter-toggle-cb").prop("checked", true);
        $("#date-filter-block").prop("className", "collapse show");

        $("#date_start").val(findGetParameter("date_start"));
        $("#date_end").val(findGetParameter("date_end"));
    }
    if (findGetParameter("lat")) {
        $("#map-filter-toggle-cb").prop("checked", true);
        $("#map-filter-block").prop("className", "collapse show");
        var lat = findGetParameter("lat");
        var lng = findGetParameter("lng");
        $.ajax({
                url: 'api/getgeobylatlong?format=json&',
                headers: {'X-CSRFToken': getCookie('csrftoken') },
                method: 'get',
                dataType: 'json',
                data: {"lat": lat, "long": lng},
                success: function(data){
                    console.log(data);
                    $("#input-find-place").val(data.name);
                    filter_marker.setLatLng({
                        "lat":data["latitude"],
                        "lng":data["longitude"]
                    });

                    $("#lat-input").val(data["latitude"]);
                    $("#lng-input").val(data["longitude"]);
                    filter_map.setView(
                        [data["latitude"], data["longitude"]], 10,
                    );


                }
            }
        );

    }




    if (findGetParameter("persons")) {
        $("#persona-filter-toggle-cb").prop("checked", true);
        $("#persona-filter-block").prop("className", "collapse show");
        person_org_tags = findGetParameter("persons").split(",");
        for (let person of person_org_tags) {
            var tag = document.createElement("span");
            tag.className = "badge badge-lg badge-default m-1";
            tag.appendChild(document.createTextNode(person));
            var i = document.createElement("i");
            i.className = "ni ni-lg ni-fat-remove";
            i.addEventListener("click", function (e) {
                $(this).parent().remove();
                person_org_tags = person_org_tags.filter(function(e) { return e !== person })
            })
            tag.appendChild(i);
            document.getElementById("taglist-persona").appendChild(tag);
        }
    }

    parent.person_org_tags = person_org_tags;
    var input_find_place = document.getElementById("input-find-place");
    var input_find_person_org = document.getElementById("input-find-person-org");
    var variant_list_place = document.getElementById("variant-list-place");
    var variant_list_persona = document.getElementById("variant-list-persona");
    var filter_search_button = document.getElementById("filter-search-button");

    $(filter_search_button).on('click', function () {
        var search = "/geo?page=1";
        if ($("#date-filter-toggle-cb").is(':checked')) {
            search = search + "&date_start=" + $("#date_start").val();
            search = search + "&date_end=" + $("#date_end").val();
        }
        if ($("#map-filter-toggle-cb").is(':checked')) {
            search = search + "&lat=" + $("#lat-input").val();
            search = search + "&lng=" + $("#lng-input").val();
        }
        if ($("#persona-filter-toggle-cb").is(':checked')) {
            search = search + "&persons=" + person_org_tags.join(",");
        }
        location.href = search;
    })
    var erase_var_loc_list = function () {
            while(variant_list_place.firstChild){
                variant_list_place.removeChild(variant_list_place.firstChild);
            }
        };
    var erase_var_pers_list = function () {
            while(variant_list_persona.firstChild){
                variant_list_persona.removeChild(variant_list_persona.firstChild);
            }
        };

     function getCookie(name) {
             var cookieValue = null;
             if (document.cookie && document.cookie != '') {
                 var cookies = document.cookie.split(';');
                 for (var i = 0; i < cookies.length; i++) {
                     var cookie = jQuery.trim(cookies[i]);
                     // Does this cookie string begin with the name we want?
                     if (cookie.substring(0, name.length + 1) == (name + '=')) {
                         cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                         break;
                     }
                 }
             }
             return cookieValue;
         }

    $(input_find_place).on('input', function (e) {
        erase_var_loc_list();
        var suggestions = [];
        // ajax to get the suggestions
        $.ajax({
            url: 'api/getgeobyname?format=json&',
            headers: {'X-CSRFToken': getCookie('csrftoken') },
            method: 'get',
            dataType: 'json',
            data: {name: input_find_place.value},
            success: function(data){
                erase_var_loc_list();
                suggestions = data;
                if (input_find_place.value.length !== 0) {
                    for (let suggestion of suggestions) {
                        var node = document.createElement("a");
                        node.className = "btn btn-block btn-outline-primary btn-choise text-dark font-weight-normal text-left";
                        $(node).on("click", function (e) {
                            //alert("Выбрано: " + $(this).text());
                            erase_var_loc_list();
                            filter_marker.setLatLng({
                                "lat":suggestion["latitude"],
                                "lng":suggestion["longitude"]
                            });
                            filter_map.setView([suggestion["latitude"], suggestion["longitude"]], 10, )
                            $("#lat-input").val(suggestion["latitude"]);
                            $("#lng-input").val(suggestion["longitude"]);
                            $(input_find_place).val(suggestion['name']);

                        })
                        node.text = suggestion['name'];
                        variant_list_place.appendChild(node);
                    }
                }
                else {
                    erase_var_loc_list();
                }
            }
        });
    });

    $(input_find_person_org).on('input', function (e) {
        erase_var_pers_list();
        var suggestions = [];
        // ajax to get the suggestions
        $.ajax({
            url: 'api/getpersonabyname?format=json&',
            headers: {'X-CSRFToken': getCookie('csrftoken') },
            method: 'get',
            dataType: 'json',
            data: {name: input_find_person_org.value},
            success: function(data){
                erase_var_pers_list();
                suggestions = data;
                if (input_find_person_org.value.length !== 0) {
                    for (let suggestion of suggestions) {

                        var node = document.createElement("a");
                        node.className = "btn btn-block btn-outline-primary btn-choise text-dark font-weight-normal text-left";
                        $(node).on("click", function (e) {
                            //alert("Выбрано: " + $(this).text());
                            erase_var_pers_list();
                            if (!person_org_tags.includes(suggestion['name'])) {
                                var tag = document.createElement("span");
                                tag.className = "badge badge-lg badge-default m-1";
                                tag.appendChild(document.createTextNode(suggestion['name']));
                                var i = document.createElement("i");
                                i.className = "ni ni-lg ni-fat-remove";
                                i.addEventListener("click", function (e) {
                                    $(this).parent().remove();
                                    person_org_tags.splice(person_org_tags.indexOf(suggestion['name']), 1);
                                })
                                tag.appendChild(i);
                                document.getElementById("taglist-persona").appendChild(tag);
                                person_org_tags.push(suggestion['name']);
                            }
                            $(input_find_person_org).val("");
                        })
                        node.text = suggestion['name'];
                        variant_list_persona.appendChild(node);
                    }
                }
                else {
                    erase_var_pers_list();
                }
            }
        });
    });
});