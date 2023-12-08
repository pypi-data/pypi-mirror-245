# Dados do FGTS
Converta os PDFs fornecidos pela [app do FGTS](https://www.fgts.gov.br/Pages/sou-trabalhador/app-fgts.aspx)
em dados estruturados num CSV prontinho para ser usado com o [Investorzilla](https://github.com/avibrazil/investorzilla).

## Instalação
```shell
pip install fgts_pdf_dados --user
```

## Uso
```shell
cd "Pasta com FGTSs"
fgts-pdf-dados
```
Ou converta os nomes das empresas para algo mais bonito:

```shell
cd "Pasta com FGTSs"
fgts-pdf-dados \
    --nickname 'C I T SOFTWARE SA' 'CI&T' \
    --nickname 'DIGITAL HOUSE EDUCACAO LTDA' 'Digital House'
```

## Resultado
O arquivo `FGTS.csv` vai conter:
| account                    | time                                |   movement |   interest |     total | desc                                    |
|:---------------------------|:------------------------------------|-----------:|-----------:|----------:|:----------------------------------------|
| FGTS CI&T (472349)         | 2019-07-05 12:00:00.898000-03:00    |     12.52  |            |           | 150-DEPOSITO JUNHO 2019                 |
| FGTS CI&T (472349)         | 2019-07-05 12:00:00.898000001-03:00 |            |            |    12.52  |                                         |
| FGTS CI&T (472349)         | 2019-08-10 12:00:00.900000-03:00    |            |       2.2  |           | CREDITO DE JAM 0,002466                 |
| FGTS CI&T (472349)         | 2019-08-10 12:00:00.900000001-03:00 |            |            |    14.72  |                                         |
| FGTS Digital House (13360) | 2019-04-04 12:00:00.808000-03:00    |     123.45 |            |           | 115-DEPOSITO MARCO 2019                 |
| FGTS Digital House (13360) | 2019-04-04 12:00:00.808000001-03:00 |            |            |    123.45 |                                         |
| FGTS Digital House (13360) | 2021-09-21 12:00:00.895000001-03:00 |            |            |      1.74 |                                         |
| FGTS Digital House (13360) | 2021-09-21 12:00:00.896000-03:00    |      -1.74 |            |           | SAQUE JAM - COD 01                      |
| FGTS Digital House (13360) | 2021-09-21 12:00:00.896000001-03:00 |            |            |      0    |                                         |

## Sobre
Feito por Avi Alkalay para prover dados pessoais ao meu painel de investimentos
do [Investorzilla](https://github.com/avibrazil/investorzilla).