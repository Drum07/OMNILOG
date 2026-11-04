package br.com.omnilog.payments; import java.math.BigDecimal; public interface ProcessadorPagamento { ResultadoPagamento processar(BigDecimal valor,String referencia); }
