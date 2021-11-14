let timer = null;
$('#id_endereco_ip').keyup(function(){
    if(validador == true){
        clearTimeout(timer);
        timer = setTimeout(VerificarEnderecoIp, 1000);
    }
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

function FormularioFuncionario(){
    AdicionarNovoItem('funcionario');
}
function FormularioTeclado(){
    AdicionarNovoItem('teclado');
}
function FormularioMouse(){
    AdicionarNovoItem('mouse');
}
function FormularioGabinete(){
    AdicionarNovoItem('gabinete');
}
function FormularioPlacaMae(){
    AdicionarNovoItem('placa_mae');
}
function FormularioProcessador(){
    AdicionarNovoItem('processador');
}
function FormularioHd(){
    AdicionarNovoItem('hd');
}
function FormularioMonitor(){
    AdicionarNovoItem('monitor');
}
function FormularioDepartamento(){
    AdicionarNovoItem('departamento', false);
}
function EditarItem(tipo){
    let lower = tipo.toLowerCase();
    let capitalize  = tipo.charAt(0).toUpperCase() + tipo.slice(1);
    const csrftoken = document.querySelector(`#form-${lower} [name=csrfmiddlewaretoken]`).value;
    var serialize = $(`#form-${lower}`).serialize();
    $.ajax({
        csrfmiddlewaretoken: csrftoken,
        type: 'POST',
        url: forms_urls[`editar_${lower}`],
        data: serialize,
        success: function(data){
            $(`#modalEdit${capitalize}`).modal('hide');
            $(`#form-${lower}`).trigger('reset');
            location.reload();
        },
        error: function (request, status, error) {
            let info = $.parseJSON(request.responseText);
            if(info['status'] == 'false'){
                alert("Verifique o formulário.");
                for(let erro_id in info['field_erros']){
                    $(`#${info['field_erros'][erro_id]}`).css('border-color', 'red');
                }
            }
        }
    })
}

function AdicionarNovoItem(tipo, requisicao=true){
    let lower = tipo.toLowerCase();
    let capitalize  = tipo.charAt(0).toUpperCase() + tipo.slice(1);
    const csrftoken = document.querySelector(`#form-${lower} [name=csrfmiddlewaretoken]`).value;
    var serialize = $(`#form-${lower}`).serialize();
    var form_ = $(`#modal${capitalize}`)

    $.ajax({
        csrfmiddlewaretoken: csrftoken,
        type: 'POST',
        url: forms_urls[`${lower}`],
        data: serialize,
        success: function(data){
            form_.modal('hide');
            $(`#form-${lower}`).trigger('reset');
            if(requisicao == true){
                Requisicao(`#id_${lower}`, `select${capitalize}`, marca=true);
            }else {
                location.reload();
            }
        },
        error: function (request, status, error) {
            let info = $.parseJSON(request.responseText);
            if(info['status'] == 'false'){
                alert("Verifique o formulário.");
                for(let erro_id in info['field_erros']){
                    $(`#${info['field_erros'][erro_id]}`).css('border-color', 'red');
                }
            }
        }
    });
}
function visualizarModalApagar(id){
    $.ajax({
        type:'GET',
        url: forms_urls['apagarDepartamento'],
        data: {
            'id': parseInt(id),
        },
        success: function(data){
            corpo = $('#modalDeletar .alerta');
            corpo.hide();
            for(let item in data){
                if(data[item] >= 1){
                    corpo.show();
                    elemento = $(`<span>- Você vai apagar ${data[item]} ${item} vinculados a esse departamento;</span><br>`);
                    corpo.append(elemento);
                }             
            }
            $('#modalDeletar').modal('show');

        },
        error: function (request, status, error) {
            let info = $.parseJSON(request.responseText);
            alert(info);
        }
    });
    $('#modalDeletar').modal('show');
}

$('#refresh-funcionario').click(()=>{ Requisicao('#id_funcionario', 'selectFuncionario', marca=true);});
$('#refresh-mouse').click(()=>{ Requisicao('#id_mouse', 'selectMouse', marca=true)});
$('#refresh-teclado').click(()=>{ Requisicao('#id_teclado', 'selectTeclado', marca=true)});
$('#refresh-monitor').click(()=>{ Requisicao('#id_monitor', 'selectMonitor')});
$('#refresh-gabinete').click(()=>{ Requisicao('#id_gabinete', 'selectGabinete', marca=true)});
$('#refresh-processador').click(()=>{ Requisicao('#id_processador', 'selectProcessador', marca=true)});
$('#refresh-placamae').click(()=>{ Requisicao('#id_placa_mae', 'selectPlacamae', marca=true)});
$('#refresh-hd').click(()=>{ Requisicao('#id_hd', 'selectHd', marca=true)});
