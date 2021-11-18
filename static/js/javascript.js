let timer = null;
let atualizarAfterModal = false;

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

$('#modalAdicionarImpressora').on('show.bs.modal', function (e) {
    PesquisarImpressoras('');    
});
$('#modalAdicionarImpressora').on('hidden.bs.modal', function(e){
    if(atualizarAfterModal == true){
        location.reload();
    }
});

$('#pesquisa').submit(function(e){
    let conteudo = $('input[name="query"]').val();
    PesquisarImpressoras(conteudo);
    return false;
})

function PesquisarImpressoras(query){
    let pesquisa = query;
    $.ajax({
        type: 'GET',
        url: forms_urls['pesquisarImpressora'],
        data: {
            'query': pesquisa,
            'id_computador': forms_urls['id_computador']
        },
        success: function(data){
            $('#tabelaImpressora').html('');
            if(data['impressoras'].length <= 0){
                $('#tabelaImpressora').append('<tr><td class="text-center">Nada encontrado.</td></tr>');
            }
            for(let item in data['impressoras']){
                let html_item = data['impressoras'][item].html_item;
                let nome = data['impressoras'][item].nome;
                let marca = data['impressoras'][item].marca;
                let ip = data['impressoras'][item].ip;

                $('#tabelaImpressora').append(
                    $(`${html_item}`)
                )
                $('#tabelaImpressora img').attr('src', `${forms_urls['m4070Img']}`);
            }
        }
    });
}
function VincularNovaImpressora(id_impressora, desvincular=false){
    $.ajax({
        type: 'GET',
        url: forms_urls['vincularNovaImpressora'],
        data: {
            'id_impressora': id_impressora,
            'id_computador': forms_urls['id_computador'],
        },
        success: function(e){
            atualizarAfterModal = true;
            if(desvincular){
                atualizarAfterModal = false;
                location.reload()
            }else{
                $(`#impressoraId${id_impressora}`).toggleClass('alert alert-success');
            }
        }
    });
}


function mandarconteudo(lowe, url=window.location){
    let capitalize  = lowe.charAt(0).toUpperCase() + lowe.slice(1);
    const csrftoken = document.querySelector(`#form-${lowe} [name=csrfmiddlewaretoken]`).value;
    var serialize = $(`#form-${lowe}`).serialize();
    $.ajax({
        csrfmiddlewaretoken: csrftoken,
        type: 'POST',
        url: url,
        data: serialize,
        success: function(data){
            $(`#modalAtualizar${capitalize}`).modal('hide');
            $(`#form-${lowe}`).trigger('reset');
            location.reload();
        },
        error: function (request, status, error) {
            console.log(request.responseText)
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

$('#refresh-funcionario').click(()=>{ Requisicao('#id_funcionario', 'selectFuncionario', marca=true);});
$('#refresh-mouse').click(()=>{ Requisicao('#id_mouse', 'selectMouse', marca=true)});
$('#refresh-teclado').click(()=>{ Requisicao('#id_teclado', 'selectTeclado', marca=true)});
$('#refresh-monitor').click(()=>{ Requisicao('#id_monitor', 'selectMonitor')});
$('#refresh-gabinete').click(()=>{ Requisicao('#id_gabinete', 'selectGabinete', marca=true)});
$('#refresh-processador').click(()=>{ Requisicao('#id_processador', 'selectProcessador', marca=true)});
$('#refresh-placamae').click(()=>{ Requisicao('#id_placa_mae', 'selectPlacamae', marca=true)});
$('#refresh-hd').click(()=>{ Requisicao('#id_hd', 'selectHd', marca=true)});
