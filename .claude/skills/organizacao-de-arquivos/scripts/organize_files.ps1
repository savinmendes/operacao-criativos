<#
.SYNOPSIS
    Copia arquivos de um plano de classificacao para uma estrutura de pastas
    por categoria, com seguranca: nunca move, nunca apaga, nunca sobrescreve.

.DESCRIPTION
    Equivalente em PowerShell de organize_files.py, para ambientes Windows
    sem Python instalado. Mesmo schema de entrada e saida — ver o cabecalho
    de organize_files.py para o formato completo do plano JSON.

.PARAMETER Plano
    Caminho para o JSON com o plano de classificacao (lista de objetos).

.PARAMETER Destino
    Pasta de destino raiz da organizacao.

.EXAMPLE
    ./organize_files.ps1 -Plano plano.json -Destino "<pasta-de-destino>"
#>

param(
    [Parameter(Mandatory = $true)]
    [string]$Plano,

    [Parameter(Mandatory = $true)]
    [string]$Destino
)

$ErrorActionPreference = "Stop"

$colunasIndice = @(
    "nome_original", "novo_nome", "extensao", "categoria", "subcategoria",
    "data_identificada", "nova_localizacao", "acao_realizada", "observacoes",
    "status_revisao"
)

function Resolve-Colisao {
    param([string]$PastaDestino, [string]$NomeArquivo)

    $candidato = Join-Path $PastaDestino $NomeArquivo
    if (-not (Test-Path -LiteralPath $candidato)) {
        return @{ Caminho = $candidato; Observacao = "" }
    }

    $stem = [System.IO.Path]::GetFileNameWithoutExtension($NomeArquivo)
    $sufixo = [System.IO.Path]::GetExtension($NomeArquivo)
    $contador = 2
    while ($true) {
        $novoNome = "${stem}_${contador}${sufixo}"
        $candidatoNovo = Join-Path $PastaDestino $novoNome
        if (-not (Test-Path -LiteralPath $candidatoNovo)) {
            return @{
                Caminho    = $candidatoNovo
                Observacao = "nome ja existia no destino; renomeado para $novoNome para nao sobrescrever"
            }
        }
        $contador++
    }
}

function Add-Observacao {
    param([string]$Existente, [string]$Nova)
    if ([string]::IsNullOrWhiteSpace($Existente)) { return $Nova }
    return "$Existente; $Nova"
}

function Process-Item {
    param($Item, [string]$DestinoRaiz)

    $origem = $Item.caminho_original
    $categoria = if ($Item.categoria) { $Item.categoria.Trim() } else { "outros" }
    $subcategoria = if ($Item.subcategoria) { $Item.subcategoria.Trim() } else { "" }
    $novoNome = if ($Item.novo_nome) { $Item.novo_nome } else { Split-Path $origem -Leaf }
    $observacoesPrevias = if ($Item.observacoes) { $Item.observacoes.Trim() } else { "" }

    $extensao = ([System.IO.Path]::GetExtension($origem)).TrimStart(".").ToLower()

    $linha = [ordered]@{
        nome_original      = Split-Path $origem -Leaf
        novo_nome          = $novoNome
        extensao           = $extensao
        categoria          = $categoria
        subcategoria       = $subcategoria
        data_identificada  = if ($Item.data_identificada) { $Item.data_identificada } else { "sem-data" }
        nova_localizacao   = ""
        acao_realizada     = ""
        observacoes        = $observacoesPrevias
        status_revisao     = if ($Item.status_revisao) { $Item.status_revisao } else { "ok" }
    }

    if (-not (Test-Path -LiteralPath $origem)) {
        $linha.acao_realizada = "erro"
        $linha.observacoes = Add-Observacao $observacoesPrevias "arquivo original nao encontrado no momento da copia"
        $linha.status_revisao = "precisa de revisao manual"
        return $linha
    }

    $pastaDestino = Join-Path $DestinoRaiz $categoria
    if ($subcategoria) { $pastaDestino = Join-Path $pastaDestino $subcategoria }
    New-Item -ItemType Directory -Force -Path $pastaDestino | Out-Null

    $resultadoColisao = Resolve-Colisao -PastaDestino $pastaDestino -NomeArquivo $novoNome
    $caminhoFinal = $resultadoColisao.Caminho

    try {
        Copy-Item -LiteralPath $origem -Destination $caminhoFinal -Force:$false -ErrorAction Stop
    }
    catch {
        $linha.acao_realizada = "erro"
        $linha.observacoes = Add-Observacao $observacoesPrevias "falha ao copiar: $($_.Exception.Message)"
        $linha.status_revisao = "precisa de revisao manual"
        return $linha
    }

    $linha.novo_nome = Split-Path $caminhoFinal -Leaf
    $linha.nova_localizacao = $caminhoFinal
    $linha.acao_realizada = "copiado"
    if ($resultadoColisao.Observacao) {
        $linha.observacoes = Add-Observacao $observacoesPrevias $resultadoColisao.Observacao
    }

    return $linha
}

if (-not (Test-Path -LiteralPath $Plano)) {
    throw "Plano nao encontrado: $Plano"
}

New-Item -ItemType Directory -Force -Path $Destino | Out-Null

$itens = Get-Content -LiteralPath $Plano -Raw -Encoding UTF8 | ConvertFrom-Json

$resultados = @()
foreach ($item in $itens) {
    $resultados += [PSCustomObject](Process-Item -Item $item -DestinoRaiz $Destino)
}

$pastaIndice = Join-Path $Destino "_indice"
New-Item -ItemType Directory -Force -Path $pastaIndice | Out-Null

$indiceJsonPath = Join-Path $pastaIndice "index.json"
$indiceCsvPath = Join-Path $pastaIndice "index.csv"
$indicePrevio = @()
if (Test-Path -LiteralPath $indiceCsvPath) {
    # Le o indice previo do CSV, nao do JSON: ConvertFrom-Json no Windows PowerShell 5.1 trunca
    # silenciosamente (sem erro) arquivos JSON grandes (acima de ~2MB), o que corrompe o indice
    # acumulado em pastas com muitos arquivos. Import-Csv nao tem esse limite.
    $indicePrevio = @(Import-Csv -LiteralPath $indiceCsvPath)
}
# O indice e cumulativo entre execucoes contra o mesmo destino: cada rodada soma ao anterior em vez de sobrescrever.
$resultadosFinais = @($indicePrevio) + @($resultados)

$resultadosFinais | ConvertTo-Json -Depth 5 | Out-File -LiteralPath $indiceJsonPath -Encoding utf8
$resultadosFinais | Select-Object $colunasIndice | Export-Csv -LiteralPath (Join-Path $pastaIndice "index.csv") -NoTypeInformation -Encoding utf8

$total = $resultados.Count
$copiados = ($resultados | Where-Object { $_.acao_realizada -eq "copiado" }).Count
$erros = ($resultados | Where-Object { $_.acao_realizada -eq "erro" }).Count
$revisao = ($resultados | Where-Object { $_.status_revisao -eq "precisa de revisao manual" }).Count

Write-Output "Total de itens no plano: $total"
Write-Output "Copiados com sucesso: $copiados"
Write-Output "Erros (arquivo original nao encontrado ou falha ao copiar): $erros"
Write-Output "Marcados como 'precisa de revisao manual': $revisao"
Write-Output "Indice salvo em: $(Join-Path $pastaIndice 'index.json') e $(Join-Path $pastaIndice 'index.csv')"
