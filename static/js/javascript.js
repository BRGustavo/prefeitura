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

$('#modalDepUser').on('show.bs.modal', function (e) {
    atualizarAfterModal = false;
    PesquisarFuncionario('');    
});
$('#modalDepUser').on('hidden.bs.modal', function (e) {
    if(atualizarAfterModal == true){
        location.reload();
    } 
});
$('#pesquisaFuncionario').submit(function(e){
    let conteudo = $("#pesquisaFuncionario").find('input[name="query"]').val();
    PesquisarFuncionario(conteudo);
    return false;
})

function PesquisarFuncionario(query){
    let pesquisa = query;
    $.ajax({
        type: 'GET',
        url: forms_urls['pesquisaFuncionario'],
        data: {
            'query': pesquisa,
            'id_computador': forms_urls['id_computador']
        },
        success: function(data){
            $('#tabelaFuncionario').html('');
           
            if(data['funcionarios'].length <= 0){
                let item_novo = $('<tr><td class="text-center">Nada encontrado.</td></tr>');
                $('#tabelaFuncionario').append(item_novo)
            }
            for(let item in data['funcionarios']){
                let html_item = data['funcionarios'][item].html_item;
                let nome = data['funcionarios'][item].nome;
                let marca = data['funcionarios'][item].marca;
                let ip = data['funcionarios'][item].ip;

                $('#tabelaFuncionario').append(
                    $(`${html_item}`)
                ).fadeIn('slow')
                $('#tabelaFuncionario img').attr('src', `${forms_urls['funcionarioImg']}`);
            }
        }
    });
}
function VincularFuncionario(id_funcionario){
    atualizarAfterModal = true
    $.ajax({
        type: 'GET',
        url: forms_urls['vincularFuncionario'],
        data: {
            'id_funcionario': id_funcionario,
            'id_computador': forms_urls['id_computador'],
        },
        success: function(e){
            let conteudo = $("#pesquisaFuncionario").find('input[name="query"]').val();
            PesquisarFuncionario(conteudo);
        }
    });
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
                let item_novo = $('<tr><td class="text-center">Nada encontrado.</td></tr>');
                $('#tabelaImpressora').append(item_novo)
            }
            for(let item in data['impressoras']){
                let html_item = data['impressoras'][item].html_item;
                let nome = data['impressoras'][item].nome;
                let marca = data['impressoras'][item].marca;
                let ip = data['impressoras'][item].ip;

                $('#tabelaImpressora').append(
                    $(`${html_item}`)
                ).fadeIn('slow')
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
            $(`#form-${lowe} input`).each(function(index){
                $(this).css('border-color', '#ced4da');
            });
            $(`#form-${lowe} label`).each(function(index){
                $(this).css('color', 'black');
            });
            let info = $.parseJSON(request.responseText);
            
            if(info['status'] == 'false'){
                alert(info['messagem']);
                for(let erro_id in info['field_erros']){
                    $(`#${info['field_erros'][erro_id]}`).css('border-color', 'red');
                    $(`label[for=${info['field_erros'][erro_id]}]`).css('color', 'red');
                }
            }
        }
    })
}
$('#modalAdicionarComputador').on('show.bs.modal', function (e) {
    $.ajax({
        type: 'GET',
        url: forms_urls.computador_novo_ajax,
        data: {
            'tipo': 'departamento'
        },
        success: function(data){
            let select = $('#departamento-departamento')
            select.html("")
            select.append($(`<option value selected'>---------</option>`))
            data['departamentos'].forEach(function(item){
                var elemento = $(`<option value='${item.id}'>${item.nome}</option>`)
                select.append(elemento);
            })
        }
    });
});

$('#form-computadornovo').submit(function(e){
    e.preventDefault()
    const csrftoken = document.querySelector(`#form-computadornovo [name=csrfmiddlewaretoken]`).value;
    let usuario = window.document.querySelector("#usuario-usuario").value
    let senha = window.document.querySelector("#senha-senha").value
    let departamento = window.document.querySelector("#departamento-departamento").value
    if(usuario !== null){
        window.document.querySelector("#id_usuario").value = usuario
        window.document.querySelector("#id_senha").value = senha
        
    }
    if(departamento !== null){
        window.document.querySelector('#id_departamento').value = departamento
    }
    var serialize = $(`#form-computadornovo`).serialize();
    $.ajax({
        csrfmiddlewaretoken: csrftoken,
        type: 'POST',
        url: forms_urls.computador_novo_ajax,
        data: serialize,
        beforeSend: function(e){

            $("#novoComputadorButton").html("<span class='spinner-border spinner-border-sm' role='status'aria-hidden='true'></span> Carregando<span class='sr-only'>Loading...</span>")
        },
        success: function(data){
            $('.modalAdicionarComputador').modal('hide')
            location.reload()
        },
        error: function (request, status, error) {
            $("#novoComputadorButton").html("Adicionar")

            $(`#form-computadornovo input`).each(function(index){
                $(this).css('border-color', '#ced4da');
            });
            $(`#form-computadornovo label`).each(function(index){
                $(this).css('color', 'black');
            });
            let info = $.parseJSON(request.responseText);
            
            if(info['status'] == 'false'){
                alert(info['messagem']);
                for(let erro_id in info['field_erros']){
                    $(`#${info['field_erros'][erro_id]}`).css('border-color', 'red');
                    $(`label[for=${info['field_erros'][erro_id]}]`).css('color', 'red');
                }
            }
        }
    })

    var serialize = $(`#form-computadornovo`).serialize();
})
$('#form-impressoranova').submit(function(e){
    e.preventDefault()
    const csrftoken = window.document.querySelector('#form-impressoranova input[name=csrfmiddlewaretoken]').value;
    var serialize = $(`#form-impressoranova`).serialize();
    $.ajax({
        csrfmiddlewaretoken: csrftoken,
        type: 'POST',
        url: forms_urls.impressora_nova_ajax,
        data: serialize,
        beforeSend: function(e){

            $("#novaImpressoraButton").html("<span class='spinner-border spinner-border-sm' role='status'aria-hidden='true'></span> Carregando<span class='sr-only'>Loading...</span>")
        },
        success: function(data){
            $('.modalImpressora').modal('hide')
            location.reload()
        },
        error: function (request, status, error) {
            $("#novaImpressoraButton").html("Adicionar")

            $(`#form-impressoranova input`).each(function(index){
                $(this).css('border-color', '#ced4da');
            });
            $(`#form-impressoranova label`).each(function(index){
                $(this).css('color', 'black');
            });
            let info = $.parseJSON(request.responseText);
            
            if(info['status'] == 'false'){
                alert(info['messagem']);
                for(let erro_id in info['field_erros']){
                    $(`#${info['field_erros'][erro_id]}`).css('border-color', 'red');
                    $(`label[for=${info['field_erros'][erro_id]}]`).css('color', 'red');
                }
            }
        }
    })
})
$('#modalImpressora').on('show.bs.modal', function(){
    window.document.querySelectorAll("#modalImpressora input:not([name='csrfmiddlewaretoken']), textarea").forEach(function(e){
        e.value = ""
    });
});
$('#form-impressoraatualizar').submit(function(e){
    e.preventDefault()
    const csrftoken = document.querySelector(`#form-impressoraatualizar [name=csrfmiddlewaretoken]`).value;
    var serialize = $(`#form-impressoraatualizar`).serialize();
    $.ajax({
        csrfmiddlewaretoken: csrftoken,
        type: 'POST',
        url: forms_urls.impressora_atualizar_ajax,
        data: serialize,
        beforeSend: function(e){

            $("#novaImpressoraButton").html("<span class='spinner-border spinner-border-sm' role='status'aria-hidden='true'></span> Carregando<span class='sr-only'>Loading...</span>")
        },
        success: function(data){
            $('.modalImpressoraAtualizar').modal('hide')
            location.reload()
        },
        error: function (request, status, error) {
            $("#novaImpressoraButton").html("Adicionar")

            $(`#form-impressoraatualizar input`).each(function(index){
                $(this).css('border-color', '#ced4da');
            });
            $(`#form-impressoraatualizar label`).each(function(index){
                $(this).css('color', 'black');
            });
            let info = $.parseJSON(request.responseText);
            
            if(info['status'] == 'false'){
                alert(info['messagem']);
                for(let erro_id in info['field_erros']){
                    $(`#${info['field_erros'][erro_id]}`).css('border-color', 'red');
                    $(`label[for=${info['field_erros'][erro_id]}]`).css('color', 'red');
                }
            }
        }
    })
})

function mostrarImpressoraAtualizar(impressora_id){
    $.ajax({
        type:"GET",
        url: forms_urls.impressora_nova_ajax,
        data: {
            'id': impressora_id
        },
        success: function(data){
            for(let item in data.campos){
                $(`input[name='${item}']`).val(data.campos[item]);
                $(`textarea[name='descricao']`).val(data.campos['descricao']);
            }
        }
    });

    $("#modalImpressoraAtualizar").modal('show');
}
function apagarImpressora(impressora_id){
    $("#modalApagarImpressora").modal('show');
    $("#modalApagarImpressora").find("#apagarID").val(impressora_id);
    
}
function confirmarRemoverImpressora(){
    let impressora_id = $("#modalApagarImpressora").find("#apagarID").val()
    $.ajax({
        type: 'GET',
        url: forms_urls.impressora_delete,
        data: {
            'impressora_id':impressora_id
        },
        success: function(data){
            $('#modalApagarImpressora').modal('hide');
            location.reload()
        }
    });
}
function apagarRoteador(roteador_id){
    $("#modalApagarRoteador").modal('show');
    $("#modalApagarRoteador").find("#apagarID").val(roteador_id);
    
}
function confirmarRemoverRoteador(){
    let roteador_id = $("#modalApagarRoteador").find("#apagarID").val()
    $.ajax({
        type: 'GET',
        url: forms_urls.roteador_delete,
        data: {
            'roteador_id':roteador_id
        },
        success: function(data){
            $('#modalApagarRoteador').modal('hide');
            location.reload()
        }
    });
}

function apagarProcessador(id_computador){
    $.ajax({
        type: 'GET',
        url: forms_urls.deletar_processador_ajax,
        data: {
            'id_computador':id_computador
        },
        success: function(data){
            $('modalRemoverProcessador').modal('hide');
            location.reload()
        },
        error: function (request, status, error) {
            let info = $.parseJSON(request.responseText);
            
            if(info['status'] == 'false'){
                alert(info['messagem']);
            }
        }
    });
}
function apagarPlacaMae(id_computador){
    $.ajax({
        type: 'GET',
        url: forms_urls.deletar_placamae_ajax,
        data: {
            'id_computador':id_computador
        },
        success: function(data){
            $('modalRemoverPlacaMae').modal('hide');
            location.reload()
        },
        error: function (request, status, error) {
            let info = $.parseJSON(request.responseText);
            
            if(info['status'] == 'false'){
                alert(info['messagem']);
            }
        }
    });
}

$('#form-roteadornovo').submit(function(e){
    e.preventDefault()
    const csrftoken = window.document.querySelector('#form-roteadornovo input[name=csrfmiddlewaretoken]').value;
    var serialize = $(`#form-roteadornovo`).serialize();
    $.ajax({
        csrfmiddlewaretoken: csrftoken,
        type: 'POST',
        url: forms_urls.roteador_add,
        data: serialize,
        beforeSend: function(e){

            $("#novoRoteadorButton").html("<span class='spinner-border spinner-border-sm' role='status'aria-hidden='true'></span> Carregando<span class='sr-only'>Loading...</span>")
        },
        success: function(data){
            $('.modalNovoRoteador').modal('hide')
            location.reload()
        },
        error: function (request, status, error) {
            $("#novoRoteadorButton").html("Adicionar")

            $(`#form-roteadornovo input`).each(function(index){
                $(this).css('border-color', '#ced4da');
            });
            $(`#form-roteadornovo label`).each(function(index){
                $(this).css('color', 'black');
            });
            let info = $.parseJSON(request.responseText);
            
            if(info['status'] == 'false'){
                alert(info['messagem']);
                for(let erro_id in info['field_erros']){
                    $(`#${info['field_erros'][erro_id]}`).css('border-color', 'red');
                    $(`label[for=${info['field_erros'][erro_id]}]`).css('color', 'red');
                }
            }
        }
    })
})
$('#modalNovoRoteador').on('show.bs.modal', function(){
    window.document.querySelectorAll("#modalNovoRoteador input:not([name='csrfmiddlewaretoken']), textarea").forEach(function(e){
        e.value = ""
    });
});

$('#form-roteadoratualizar').submit(function(e){
    e.preventDefault()
    const csrftoken = window.document.querySelector('#form-roteadoratualizar input[name=csrfmiddlewaretoken]').value;
    var serialize = $(`#form-roteadoratualizar`).serialize();
    $.ajax({
        csrfmiddlewaretoken: csrftoken,
        type: 'POST',
        url: forms_urls.roteador_edit,
        data: serialize,
        beforeSend: function(e){

            $("#novoRoteadorButton").html("<span class='spinner-border spinner-border-sm' role='status'aria-hidden='true'></span> Carregando<span class='sr-only'>Loading...</span>")
        },
        success: function(data){
            $('.modalAtualizarRoteador').modal('hide')
            location.reload()
        },
        error: function (request, status, error) {
            $("#novoRoteadorButton").html("Adicionar")

            $(`#form-roteadoratualizar input`).each(function(index){
                $(this).css('border-color', '#ced4da');
            });
            $(`#form-roteadoratualizar label`).each(function(index){
                $(this).css('color', 'black');
            });
            let info = $.parseJSON(request.responseText);
            
            if(info['status'] == 'false'){
                alert(info['messagem']);
                for(let erro_id in info['field_erros']){
                    
                    $(`#${info['field_erros'][erro_id]}`).each(function(){
                        $(this).css('border-color', 'red');
                    })
                    $(`label[for=${info['field_erros'][erro_id]}]`).css('color', 'red');
                }
            }
        }
    })
})

function atualizarRoteador(roteador_id){
    $.ajax({
        type: 'GET',
        url: forms_urls.roteador_edit,
        data: {
            'roteador_id': roteador_id
        },
        success: function(data){
            campos = data['campos']
            for(let item in campos){
                $(`[name=${item}]`).val(campos[item])
            }
            $('#modalAtualizarRoteador').modal('show');
        },
    });
}

$('#removerPc').click(function(e){
    data = {
        'id_computador': forms_urls.id_computador,
    }
    lista_ids = ['manterGabinete', 'manterMonitor', 'manterHd', 'manterPlacaMae', 'manterProcessador', 'manterMemoriaRam']
    for(let item in lista_ids){
        
        if($(`#${lista_ids[item]}`).is(':checked')){
            data[lista_ids[item]] = 'Sim'
        }else {
            data[lista_ids[item]] = 'Não'
        }
    }
    $.ajax({
        type: 'GET',
        data: data,
        url: forms_urls.computador_remover,
        success: function(data){
            $('#modalRemoverPc').modal('hide');
            window.location.href = forms_urls.computador_view;
        },
        error: function (request, status, error) {
            let info = $.parseJSON(request.responseText)
            if(info['messagem'].length >=1){
                for(let item in info['messagem']){
                    alert(info['messagem'][item])
                }
            }else {
                alert('Ocorreu um erro ao tentar remover o PC.')
            }
        }
    });
})

// Ativando Modal Deletar Informações do Funcionário.
function ModalRemoverFuncionario(url=false){
    $('#modalDeletar').modal('show');
    if(url != false){
        $('#modalDeletar #linkRemoverFuncionario').attr('href', url)
    }
}
// Ativando Modal Atualizar Informações do Funcionário.
function ModalAtualizarFuncionario(id_funcionario, url){
    $('#modalEditFuncionario').modal('show');
    $.ajax({
        type: 'GET',
        url: url,
        data: {
            'id': id_funcionario
        },
        success: function(data){
            $('#modalEditFuncionario #id_nome').val(data.id_nome);
            $('#modalEditFuncionario #id_sobrenome').val(data.id_sobrenome);
            $('#modalEditFuncionario #id_senha_pc').val(data.id_senha_pc);
            $('#modalEditFuncionario #id_usuario_pc').val(data.id_usuario_pc);
            $('#modalEditFuncionario #id_controle_acesso').val(data.id_controle_acesso);
            $('#modalEditFuncionario #id_admin_rede').val(data.id_adm_rede);
            $('#modalEditFuncionario #id_descricao').val(data.id_descricao);
            $('#modalEditFuncionario #EditarFuncionario').attr('onclick', data.url);

            for(let departamento in data.departamentos){
                $('#modalEditFuncionario #id_departamento').append(`<option value="${data.departamentos[departamento].id}">${data.departamentos[departamento].valor}</option>`);
            }
            $(`#modalEditFuncionario #id_departamento option[value='${data.departamento}']`).attr("selected", "selected");
        },
        error: function(response, status, error){
            alert('Não possivel concluir a operação. Atualize a página.')
        }
    })
    
}
function UpdateFuncionario(url){
    const csrftoken = document.querySelector(`#form-funcionario [name=csrfmiddlewaretoken]`).value;
    var serialize = $(`#modalEditFuncionario #form-funcionario`).serialize();
    $.ajax({
        csrfmiddlewaretoken: csrftoken,
        type: 'POST',
        url: url,
        data: serialize,
        success: function(data){
            $(`#modalEditFuncionario`).modal('hide');
            $(`#form-funcionario`).trigger('reset');
            location.reload();
        },
        error: function (request, status, error) {
            let info = $.parseJSON(request.responseText);
            if(info['status'] == 'false'){
                alert("Verifique o formulário.");
                for(let erro_id in info['field_erros']){
                    $(`#modalEditFuncionario #${info['field_erros'][erro_id]}`).css('border-color', 'red');
                }
            }
        }
    })
}
function ModalRemoverUsuario(id){
    $('#modalRemoverFuncionario').modal('show');
    $('#modalRemoverFuncionario #btnRemover').attr('onclick', `RemoverUsuario('${id}')`)
}
function RemoverUsuario(id){
    $.ajax({
        type: 'GET',
        url: form_urls.remover_usuario_ajax,
        data: {
            'id': id,

        },
        success: function(data){
            $('#modalRemoverFuncionario').modal('hide');
            location.reload();
        },
        error: function(request, status, error){
            let info = $.parseJSON(request.responseText);
            if(info['mensagem'].length >=1){
                alert(info['mensagem']);
            }else {
                alert('Não foi possivel concluir essa operação.')
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
