function SetCookie(cookieName,cookieValue,nDays) {
    var today = new Date();
    var expire = new Date();
    if (nDays==null || nDays==0) nDays=1;
    expire.setTime(today.getTime() + 3600000*24*nDays);
    document.cookie = cookieName+"="+escape(cookieValue)
    + ";expires="+expire.toGMTString();
}

function ReadCookie(cookieName) {
    var theCookie=" "+document.cookie;
    var ind=theCookie.indexOf(" "+cookieName+"=");
    if (ind==-1) ind=theCookie.indexOf(";"+cookieName+"=");
    if (ind==-1 || cookieName=="") return "";
    var ind1=theCookie.indexOf(";",ind+1);
    if (ind1==-1) ind1=theCookie.length;
    return unescape(theCookie.substring(ind+cookieName.length+2,ind1));
}

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

    ModoApresentacao('');

    $("#btn_font_menos").click(function() {
        $(".container-cifra").css("font-size", "-=1");
    });
    $("#btn_font_mais").click(function() {
        $(".container-cifra").css("font-size", "+=1");
    });

    var timeCalc = 300;
    var timeDirec = 1;
    var timeIntervals = [];

    function iniciarDeslocamento() {
        timeIntervals.push(setInterval(function() {
            window.scrollTo(20, window.pageYOffset+timeDirec);
            },timeCalc));
    }
    function pararDeslocamento() {
        while (timeIntervals.length > 0)
            clearInterval(timeIntervals.shift());
    }
    function reiniciarDeslocamento() {
        pararDeslocamento();
        iniciarDeslocamento();
    }
    $('.velocidade').bind('mouseenter', function(e) {
        iniciarDeslocamento();
        $(".velocidade").stop().animate({"width": "99%"},1600);
        $(".meioControleVelocidade").stop().animate({"top":
            parseInt(  $(".velocidade").css("height").substring(0,$(".velocidade").css("height").length-2)/2-25
            )
     },1600);
    });
    $('.velocidade').bind('mouseleave', function(e) {
        pararDeslocamento();
        $(".velocidade").stop().animate({"width": "5px"},1600);
        $(".meioControleVelocidade").stop().animate({"top": "-52px"},1600);
    });
    $('.velocidade').bind('click', function(e) {
        pararDeslocamento();
        $(".velocidade").stop().css("width", "5px");
        $(".meioControleVelocidade").stop().css("top", "-52px");
    });
    $('.velocidade').bind('mousemove', function(event) {
        var heightCaixa = this.clientHeight;
        var posCaixa = event.clientY;
        var val = (posCaixa - heightCaixa / 2);

        if (val < 0) {
            timeDirec = -2;
            val = Math.abs(val);
        }
        else {
            timeDirec = 2;
            reiniciarDeslocamento();
        }
        var taxa = (val) / (heightCaixa / 2);
        timeCalc = 500 * (1 - taxa * taxa);

        //console.log(heightCaixa+" - "+posCaixa+" - "+taxa+" - "+timeCalc);
        if (val <= 25)
            pararDeslocamento();
        else
            reiniciarDeslocamento();
    });

});

function ModoApresentacao(modo) {
    var modo_apresentacao = ReadCookie("modo_apresentacao");
    if (modo_apresentacao != '') {
        $('.btn-modo-apresentacao').addClass(modo_apresentacao);
        aplicarFluid();
    }

    function aplicarFluid() {
        $('nav > div.container').removeClass('container').addClass('container-fluid');
        $('header > div.container').removeClass('container').addClass('container-fluid');
        $('main > div.container').removeClass('container').addClass('container-fluid');
        $('footer > div.container').removeClass('container').addClass('container-fluid');
    }

    function removerFluid() {
        $('nav > div.container-fluid').removeClass('container-fluid').addClass('container');
        $('header > div.container-fluid').removeClass('container-fluid').addClass('container');
        $('main > div.container-fluid').removeClass('container-fluid').addClass('container');
        $('footer > div.container-fluid').removeClass('container-fluid').addClass('container');
    }

    function toogleModo() {
        $('.btn-modo-apresentacao').toggleClass('paisagem');
        modo_apresentacao = $('.btn-modo-apresentacao').hasClass('paisagem') ? 'paisagem': '';
        SetCookie("modo_apresentacao", modo_apresentacao, 30);
        if (modo_apresentacao == '')
            removerFluid();
        else
            aplicarFluid();
    }

    $('.btn-modo-apresentacao').on('click', function() {
        toogleModo();
    });
}
