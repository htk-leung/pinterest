let dropdownBtn = document.getElementById("dropdown-text")
let list = document.getElementById("droplist")
let icon = document.getElementById("dropicon");
let span = document.getElementById("category");
let input = document.getElementById("search-input");
let listitems = document.querySelectorAll(".dropdown-list-item");
let searchForm = document.getElementById("search-form"); // Get the form element
let selectedCategory = span.innerText; // Track the selected category (default to the first item's text)

//show dropdown
dropdownBtn.onclick = function() {
    if (list.classList.contains("show")) {
        icon.style.rotate = "0deg";
    } else {
        icon.style.rotate = "-180deg";
    }
    list.classList.toggle("show");
    e.stopPropagation(); // Prevent the window click event from firing
};

// rotate arrow back, hide dropdown
window.onclick = function(e) {
    if(
        e.target.id !== "dropdown-text" &&
        e.target.id !== "droplist" &&
        e.target.id !== "dropicon"
    ) {
        list.classList.remove("show");
        icon.style.rotate = "0deg";
    }
}

for(item of listitems) {
    item.onclick=function(e){
        // change dropdown display text
        span.innerText=e.target.innerText;
        // Update the hidden form field with the selected category
        document.getElementById("selected-category").value = span.innerText;
        selectedCategory = span.innerText;
    }
}

document.addEventListener('DOMContentLoaded', function() {
    const searchForm = document.getElementById('search-form');
    const searchIcon = searchForm.querySelector('.search-box svg');
    
    // Add click event to the search icon
    searchIcon.addEventListener('click', function() {
        searchForm.submit();
    });
});

searchForm.addEventListener('submit', 
    function(e) {
        if (input.value.trim() === "") {
            e.preventDefault(); // Prevent form submission if search is empty
            input.focus();
            return false;
        }
    
    console.log("Submitting search:", {
        category: selectedCategory,
        searchTerm: input.value
    });
})