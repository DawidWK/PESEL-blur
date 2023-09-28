// Add event listener on change of input [name=file] and if file is selected, change the text of the label
document.querySelector('input[name=file]').addEventListener('change', function(e) {
    if (this.files[0]) {
        document.querySelector('#noFile').innerHTML = this.files[0].name;
    } else {
        document.querySelector('#noFile').innerHTML = "No file chosen...";
    }
});