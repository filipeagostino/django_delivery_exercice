// DELETE ITEM

$(document).ready(function() {
    var deleteBtn = $('.delete-btn');
    var searchBtn = $('#search-btn');
    var searchForm = $('#search-form');

    $(deleteBtn).on('click', function(e) {

        e.preventDefault();

        var delLink = $(this).attr('href');
        var result = confirm('Really want to delete this item??');

        if(result) {
            window.location.href = delLink;
        }

    });

    $(searchBtn).on('click', function() {
        searchForm.submit();

    });
});

// CHECK CEP

var zip_code = document.getElementsByName("zip_code")[0];


$(zip_code).focusout(function () {
    temp = zip_code.value;
    zip_code_formated = `${temp.slice(0, 5)}-${temp.slice(5, 8)}`

    console.log(`zip code: ${zip_code.value}`);
    console.log(`zip_code_formated: ${zip_code_formated}`);
    var xhr = new XMLHttpRequest();
 
    xhr.open("GET", `https://cdn.apicep.com/file/apicep/${zip_code_formated}.json`);
 
    xhr.addEventListener("load", function() {
 
        if (xhr.status == 200) {
            var response = xhr.responseText;
            var data = JSON.parse(response);
            console.log(data);
            document.getElementsByName("address")[0].value = data['address'];
            document.getElementsByName("city")[0].value = data['city'];
            document.getElementsByName("district")[0].value = data['district'];
        
        } else {
            document.getElementsByName("address")[0].value = '';
            document.getElementsByName("city")[0].value = '';
            document.getElementsByName("district")[0].value = '';
            alert('Invalid Cep!');
            
        }
    });
    xhr.send();
});

// GET DB VALUES WITH PYTHON AND AUTOCOPLETE FORM FIELDS WITH JS

var product = document.getElementsByName("product")[0];

$(product).change(function () {
    data = product.value
    console.log(data)
    
    $.getJSON(`http://127.0.0.1:8000/shipping/djangowebservice/${data}`, (data) => {
        console.log(data);
        document.getElementsByName("deadline")[0].value = data['prazopac'];
        document.getElementsByName("price")[0].value = parseFloat(data['valorpac']);
    });
});
