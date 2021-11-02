let timer = null;
$('#id_endereco_ip').keyup(function(){
    clearTimeout(timer);
    timer = setTimeout(VerificarEnderecoIp, 1000);
});
function VerificarEnderecoIp(){
    var ip_valor = window.document.querySelector('#id_endereco_ip').value;
    if(ip_valor.length >= 1){
        $.ajax({
            url: ip_form_url_ajax,
            data: {
                'enderecoip': `${ip_valor}`
            },
            dataType: 'json',
            success: function(data){
                if(data['valido'] == true){
                    $('#id_endereco_ip').css('border-color', 'green');
                    $('#btnenviar').prop('disabled', false);
                    $('#enderecoiphelp').html('')
                }else {
                    $('#id_endereco_ip').css('border-color', 'red');
                    $('#btnenviar').prop('disabled', true);
                    $('#enderecoiphelp').html(`* ${data['mensagem']}`);
                }
            }
        });
    }else {
        $('#id_endereco_ip').css('border-color', '#ced4da');
        $('#btnenviar').prop('disabled', false);
        $('#enderecoiphelp').html('')
    }
}

function Requisicao(seletor, input, marca=false) {
    let selectorSelecionado = $(`${seletor}`);
    $.ajax({
        url: computador_form_url_ajax,
        data: {
            'tipoValue': `${input}`
        },
        dataType: 'json',
        success: function(data){
            $(`${seletor}`).empty();
            if(marca == true){
                selectorSelecionado.append($(`<option value selected'>---------</option>`));
                }
            if(data.length >= 1){

            }
            for(let item in data){
                var elemento = $(`<option value='${data[item][0]}'>${data[item][1]}</option>`)
                selectorSelecionado.append(elemento);
            }
        }
    });
}
$('#refresh-funcionario').click(()=>{ Requisicao('#id_funcionario', 'selectFuncionario', marca=true);});
$('#refresh-mouse').click(()=>{ Requisicao('#id_mouse', 'selectMouse', marca=true)});
$('#refresh-teclado').click(()=>{ Requisicao('#id_teclado', 'selectTeclado', marca=true)});
$('#refresh-monitor').click(()=>{ Requisicao('#id_monitor', 'selectMonitor')});
$('#refresh-gabinete').click(()=>{ Requisicao('#id_gabinete', 'selectGabinete', marca=true)});
$('#refresh-processador').click(()=>{ Requisicao('#id_processador', 'selectProcessador', marca=true)});
$('#refresh-placamae').click(()=>{ Requisicao('#id_placa_mae', 'selectPlacamae', marca=true)});
$('#refresh-hd').click(()=>{ Requisicao('#id_hd', 'selectHd', marca=true)});
