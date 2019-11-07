
<script>
var modal;
function abrir_modal(url, titulo)
{
    modal = $('#popup').dialog(
    {
        title: titulo,
        modal: true,
        width: 500,
        resizable: false,
        
    }).dialog('open').load(url)
}

function cerrar_modal()
{
    modal.dialog("close");
}

$(document).ready(function()
{
    var table = $('#tabla').dataTable( {
        "language": {
        	url: "/static/localizacion/es_ES.json"
        }
    } );
});
</script>