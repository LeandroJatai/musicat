function initTinymce(elements) {
    removeTinymce();
    var config_tinymce = {
        force_br_newlines : false,
        force_p_newlines : false,
        forced_root_block : '',
        plugins: ["table save code"],
        menubar: "edit format table tools",
        toolbar: "undo redo | styleselect | bold italic | alignleft aligncenter alignright alignjustify | bullist numlist outdent indent",
        tools: "inserttable",
        border_css: "/static/styles/style_tinymce.css",
        content_css: "/static/styles/style_tinymce.css",
    }
    if (elements != null) {
        config_tinymce['elements'] = elements;
        config_tinymce['mode'] = "exact";
        }
    else
        config_tinymce['mode'] = "textareas";

    tinymce.init(config_tinymce);
}

function removeTinymce() {
    while (tinymce.editors.length > 0) {
        tinymce.remove(tinymce.editors[0]);
    }
}

function refreshDatePicker() {
    $.datepicker.setDefaults($.datepicker.regional['pt-BR']);
    $('.dateinput').datepicker();
}

function refreshMask() {
    $('.telefone').mask("(99) 9999-9999", {placeholder:"(__) ____ -____"});
    $('.cpf').mask("000.000.000-00", {placeholder:"___.___.___-__"});
    $('.cep').mask("00000-000", {placeholder:"_____-___"});
    $('.rg').mask("0.000.000", {placeholder:"_.___.___"});
    $('.titulo_eleitor').mask("0000.0000.0000.0000", {placeholder:"____.____.____.____"});
    $('.dateinput').mask('00/00/0000', {placeholder:"__/__/____"});
    $('.hora').mask("00:00", {placeholder:"hh:mm"});
    $('.hora_hms').mask("00:00:00", {placeholder:"hh:mm:ss"});
}


$(document).ready(function(){
    refreshDatePicker();
    refreshMask();
    initTinymce("texto-rico");
    
    $("input[name='search']").focus();
});
